import json, sys
p=sys.argv[1] if len(sys.argv)>1 else 'security_ethical_hacking_pack.json'
d=json.load(open(p,encoding='utf-8'))
ls=d['lessons']; u=[x['uid'] for x in ls]
assert len(ls)==110, len(ls)
assert len(set(u))==len(u), 'duplicate uid'
for x in ls:
    for k in ['uid','chapter_order','subchapter_order','lesson_order','title_fa','title_en','summary','full_content','meta']:
        assert k in x, (x.get('uid'),k)
    a=x['meta']['assessment']
    assert len(a['questions'])==4
    assert all(q['id'] in a['answer_key'] for q in a['questions'])
    assert all(q['id'] not in q for q in a['questions'])
print(f'OK: {len(ls)} lessons; {len(set(u))} unique UIDs; questions and answer keys separated; chapter={d["compatibility"]["chapter_order"]}')
