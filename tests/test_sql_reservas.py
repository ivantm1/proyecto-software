def test_sql_contains_caducada():
    with open('SQLQuery1.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    assert 'Caducada' in sql


def test_pruebas_contains_caducada_comment():
    with open('pruebas.sql', 'r', encoding='utf-8') as f:
        txt = f.read()
    assert 'Caducada' in txt
