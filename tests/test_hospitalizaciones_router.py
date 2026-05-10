def test_crear_hospitalizacion_urgencia_no_existe(client):
    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":999
    })
    assert response.status_code == 400
    assert response.json()["message"] == "La atención de urgencias no existe"

def test_crear_hospitalizacion_atencion_ya_existe(client,crear_urgencia,crear_hospitalizacion):

    urgencia = crear_urgencia
    hospitalziacion= crear_hospitalizacion

    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":urgencia.id_urgencia
    })
    assert response.status_code == 400
    assert response.json()["message"] == "Ya existe una hospitalización para esta atención de urgencias"

def test_crear_hospitalizacion_exitoso(client,borrar_hospitalizaciones):
    #Toca borrar las hospitalizaciones para que no exista una hospitalización previa a la urgencia con id 50
    response = client.post("/api/hospitalizacion", json={
        "id_urgencia":50
    })
    assert response.status_code == 201
    assert response.json()["data"]["id_urgencia"] == 50