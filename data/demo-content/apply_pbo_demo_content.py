"""Applies data/demo-content/pbo-demo-content.json to an org, per the decisions saved from the review form.

Usage: python3 data/demo-content/apply_pbo_demo_content.py <org alias> <phase> [--dry-run]
Phases, in order: locations, campaigns, jobs, newshifts, shiftrules, skills
Idempotent: locations are matched by Name, campaigns and jobs by Name, new shifts by job + start time.
"""
import json, sys, subprocess, urllib.request, urllib.parse, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent
DRAFT = json.loads((HERE / 'pbo-demo-content.json').read_text())
ANSWERS = json.loads((HERE.parents[1] / '_plans/pbo-demo-content/pbo-demo-content-review-answers.json').read_text())
DECIDED = {r['headline']: r for r in ANSWERS['rows']}
ORG, PHASE = sys.argv[1], sys.argv[2]
DRY = '--dry-run' in sys.argv

def sf_json(args):
    out = subprocess.run(['sf', *args, '--json'], capture_output=True, text=True).stdout
    return json.loads(out)['result']

auth = sf_json(['org', 'display', '--target-org', ORG])
BASE = auth['instanceUrl'] + '/services/data/v65.0'
HEADERS = {'Authorization': 'Bearer ' + auth['accessToken'], 'Content-Type': 'application/json'}

def rest(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, headers=HEADERS, data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req) as r: return json.loads(r.read() or b'null')
    except urllib.error.HTTPError as e:
        raise SystemExit(f'{method} {path} failed {e.code}: {e.read().decode()[:800]}')

def query(soql): return rest('GET', '/query?q=' + urllib.parse.quote(soql))['records']

def collection(method, records, size=200):
    """sobject collections, allOrNone; size=1 keeps each record in its own transaction for heavy triggers"""
    done = []
    for i in range(0, len(records), size):
        chunk = records[i:i + size]
        if DRY: print(f'  DRY {method} {len(chunk)} records, first: {json.dumps(chunk[0])[:300]}'); continue
        res = rest(method, '/composite/sobjects', {'allOrNone': True, 'records': chunk})
        bad = [r for r in res if not r['success']]
        if bad: raise SystemExit('collection errors: ' + json.dumps(bad[:3], indent=1))
        done += res
    return done

def decided(headline): return DECIDED.get(headline, {}).get('decision', 'add')
def field_value(headline, key, fallback):
    return DECIDED.get(headline, {}).get('fields', {}).get(key, fallback)

loc_by_key = {l['key']: l for l in DRAFT['locations']}

if PHASE == 'locations':
    rt = query("SELECT Id FROM RecordType WHERE SobjectType='Account' AND DeveloperName='Organization'")[0]['Id']
    existing = {a['Name']: a['Id'] for a in query("SELECT Id, Name FROM Account WHERE Type='Demo Volunteer Organization'")}
    creates, updates = [], []
    for l in DRAFT['locations']:
        if decided(l['Name']) == 'skip': print('skip', l['Name']); continue
        rec = {'attributes': {'type': 'Account'}, 'RecordTypeId': rt, 'Type': 'Demo Volunteer Organization', 'FlowToolKit__cUnite_Volunteer_Location__c': True}
        for k in ('Name', 'ShippingStreet', 'ShippingCity', 'ShippingState', 'ShippingPostalCode', 'ShippingCountry', 'Description'):
            rec[k] = field_value(l['Name'], k, l[k])
        for k in ('Street', 'City', 'State', 'PostalCode', 'Country'): rec['Billing' + k] = rec['Shipping' + k]
        if rec['Name'] in existing: rec['Id'] = existing[rec['Name']]; updates.append(rec)
        else: creates.append(rec)
    print(f'locations: {len(creates)} to create, {len(updates)} to update')
    if creates: collection('POST', creates)
    if updates: collection('PATCH', updates)

elif PHASE == 'campaigns':
    by_name = {c['Name']: c['Id'] for c in query("SELECT Id, Name FROM Campaign WHERE Id IN (SELECT GW_Volunteers__Campaign__c FROM GW_Volunteers__Volunteer_Job__c)")}
    updates = []
    for c in DRAFT['campaigns']:
        if decided(c['Name']) == 'skip': print('skip', c['Name']); continue
        rec = {'attributes': {'type': 'Campaign'}, 'Id': by_name[c['Name']]}
        for k, v in c.items():
            if k == 'Name': continue
            rec[k] = field_value(c['Name'], k, v)
        updates.append(rec)
    print(f'campaigns: {len(updates)} to update')
    collection('PATCH', updates)

elif PHASE == 'jobs':
    accounts = {a['Name']: a['Id'] for a in query("SELECT Id, Name FROM Account WHERE Type='Demo Volunteer Organization'")}
    campaigns = {c['Name']: c['Id'] for c in query("SELECT Id, Name FROM Campaign WHERE Id IN (SELECT GW_Volunteers__Campaign__c FROM GW_Volunteers__Volunteer_Job__c)")}
    jobs = {j['Name']: j['Id'] for j in query("SELECT Id, Name FROM GW_Volunteers__Volunteer_Job__c")}
    skills_live = {v['value'] for v in [f for f in sf_json(['sobject', 'describe', '--sobject', 'GW_Volunteers__Volunteer_Job__c', '--target-org', ORG])['fields'] if f['name'] == 'GW_Volunteers__Skills_Needed__c'][0]['picklistValues'] if v['active']}
    updates, skills_deferred = [], []
    content_keys = ('FlowToolKit__cUnite_Subtitle__c', 'GW_Volunteers__Description__c', 'Excerpt__c', 'GW_Volunteers__Location_Information__c', 'FlowToolKit__cUnite_Confirmation_Page_Message__c')
    for j in DRAFT['jobs']:
        if decided(j['Name']) == 'skip': print('skip', j['Name']); continue
        loc = loc_by_key[j['location']]
        rec = {'attributes': {'type': 'GW_Volunteers__Volunteer_Job__c'}, 'Id': jobs[j['Name']],
               'FlowToolKit__cUnite_Location__c': accounts[loc['Name']],
               'FlowToolKit__cUnite_Location_Name__c': loc['Name'],
               'GW_Volunteers__Location_Street__c': loc['ShippingStreet'],
               'GW_Volunteers__Location_City__c': loc['ShippingCity'],
               'GW_Volunteers__Location__c': loc['ShippingState'],
               'GW_Volunteers__Location_Zip_Postal_Code__c': loc['ShippingPostalCode'],
               'FlowToolKit__cUnite_Location_Country__c': loc['ShippingCountry'],
               'GW_Volunteers__Volunteer_Website_Time_Zone__c': loc['timeZone'],
               'Remote__c': j['Remote__c'], 'GW_Volunteers__Ongoing__c': j['GW_Volunteers__Ongoing__c']}
        for k in content_keys:
            if j.get(k): rec[k] = field_value(j['Name'], k, j[k])
        for k in ('GW_Volunteers__Display_on_Website__c', 'FlowToolKit__cUnite_Volunteer_Types__c'):
            if k in j: rec[k] = j[k]
        if j.get('campaign'): rec['GW_Volunteers__Campaign__c'] = campaigns[j['campaign']]
        if ANSWERS['answers']['accepting'] == 'yes': rec['FlowToolKit__cUnite_Accepting_Applications__c'] = True
        skill = j.get('GW_Volunteers__Skills_Needed__c') or j.get('skillsIfOptionA')
        if skill and skill in skills_live: rec['GW_Volunteers__Skills_Needed__c'] = skill
        elif skill: skills_deferred.append((j['Name'], skill))
        updates.append(rec)
    print(f'jobs: {len(updates)} to update; skills deferred (value not in picklist yet): {skills_deferred}')
    collection('PATCH', updates, size=1)  # the Sync Shift Confirmation Message flow touches every shift of the job

elif PHASE == 'skills':
    jobs = {j['Name']: j['Id'] for j in query("SELECT Id, Name FROM GW_Volunteers__Volunteer_Job__c")}
    skills_live = {v['value'] for v in [f for f in sf_json(['sobject', 'describe', '--sobject', 'GW_Volunteers__Volunteer_Job__c', '--target-org', ORG])['fields'] if f['name'] == 'GW_Volunteers__Skills_Needed__c'][0]['picklistValues'] if v['active']}
    updates, missing = [], set()
    for j in DRAFT['jobs']:
        skill = j.get('skillsIfOptionA')
        if not skill or decided(j['Name']) == 'skip': continue
        if skill in skills_live: updates.append({'attributes': {'type': 'GW_Volunteers__Volunteer_Job__c'}, 'Id': jobs[j['Name']], 'GW_Volunteers__Skills_Needed__c': skill})
        else: missing.add(skill)
    print(f'skills: {len(updates)} jobs to update; still missing from the picklist: {sorted(missing)}')
    if updates: collection('PATCH', updates)

elif PHASE == 'newshifts':
    jobs = {j['Name']: j['Id'] for j in query("SELECT Id, Name FROM GW_Volunteers__Volunteer_Job__c")}
    def utc(local_iso, tz):
        from zoneinfo import ZoneInfo
        dt = datetime.datetime.fromisoformat(local_iso).replace(tzinfo=ZoneInfo(tz))
        return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000+0000')
    wanted = []
    if ANSWERS['answers']['gala'] == 'yes':
        for s in DRAFT['galaShifts']['shifts']:
            wanted.append({'job': s['job'], 'start': utc(s['start'], 'America/Chicago'), 'hours': s['durationHours'], 'desired': s['desired'], 'desc': s['job'] + ' team, ' + DRAFT['galaShifts']['eventDate']})
    if ANSWERS['answers']['neighborhood'] == 'rebuild':
        for d in DRAFT['neighborhoodCleanupShifts']['dates']:
            wanted.append({'job': 'Neighborhood Cleanup', 'start': utc(d + 'T09:00:00', 'America/Chicago'), 'hours': 3, 'desired': 25, 'desc': 'Last Saturday block cleanup'})
    job_ids = tuple(sorted({jobs[w['job']] for w in wanted}))
    existing = {(s['GW_Volunteers__Volunteer_Job__c'], s['GW_Volunteers__Start_Date_Time__c']) for s in query(f"SELECT GW_Volunteers__Volunteer_Job__c, GW_Volunteers__Start_Date_Time__c FROM GW_Volunteers__Volunteer_Shift__c WHERE GW_Volunteers__Volunteer_Job__c IN {job_ids}")}
    creates = [{'attributes': {'type': 'GW_Volunteers__Volunteer_Shift__c'}, 'GW_Volunteers__Volunteer_Job__c': jobs[w['job']], 'GW_Volunteers__Start_Date_Time__c': w['start'],
                'GW_Volunteers__Duration__c': w['hours'], 'GW_Volunteers__Desired_Number_of_Volunteers__c': w['desired'], 'GW_Volunteers__Description__c': w['desc']}
               for w in wanted if (jobs[w['job']], w['start']) not in existing]
    print(f'new shifts: {len(wanted)} wanted, {len(creates)} to create')
    if creates: collection('POST', creates)

elif PHASE == 'shiftrules':
    mode = ANSWERS['answers']['shifts']
    if mode == 'none': raise SystemExit('shift rules: declined')
    subtitles = DRAFT['shiftRules']['subtitleByTimeOfDay']; fallback = DRAFT['shiftRules']['subtitleFallback']
    job_sub = {j['Name']: field_value(j['Name'], 'FlowToolKit__cUnite_Subtitle__c', j['FlowToolKit__cUnite_Subtitle__c']) for j in DRAFT['jobs']}
    shifts = query("SELECT Id, FlowToolKit__cUnite_Time_of_Day__c, FlowToolKit__cUnite_Subtitle__c, GW_Volunteers__Description__c, GW_Volunteers__Volunteer_Job__r.Name FROM GW_Volunteers__Volunteer_Shift__c WHERE GW_Volunteers__Start_Date_Time__c >= LAST_N_DAYS:30")
    rows = []
    for s in shifts:
        row = {'Id': s['Id'], 'FlowToolKit__cUnite_Subtitle__c': subtitles.get(s['FlowToolKit__cUnite_Time_of_Day__c'], fallback)}
        if mode == 'both' and not s['GW_Volunteers__Description__c']:
            row['GW_Volunteers__Description__c'] = job_sub.get(s['GW_Volunteers__Volunteer_Job__r']['Name'], '')
        rows.append(row)
    print(f'shift rules: {len(rows)} shifts, {sum(1 for r in rows if "GW_Volunteers__Description__c" in r)} get a description')
    for r in rows: r['attributes'] = {'type': 'GW_Volunteers__Volunteer_Shift__c'}
    collection('PATCH', rows)
    print('shift rules applied')
else:
    raise SystemExit('unknown phase ' + PHASE)
