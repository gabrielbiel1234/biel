function buscarInformacoes() {
    var cpf = document.getElementById('cpf').value;
    if (cpf.length === 11) {
        fetch(`https://api.tds-locais.com.br/consulta/cpf/${cpf}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('resultado').innerHTML = `<p>Nome: ${data.nome}</p><p>Endereço: ${data.endereco}</p><p>CEP: ${data.cep}</p><p>Telefone: ${data.telefone}</p><p>UF: ${data.uf}</p><p>Cidade: ${data.cidade}</p><p>Estado: ${data.estado}</p><p>País: ${data.pais}</p>`;
                } else {
                    document.getElementById('resultado').innerHTML = `<p>Erro ao buscar informações do CPF</p>`;
                }
            })
            .catch(error => {
                document.getElementById('resultado').innerHTML = `<p>Erro ao buscar informações do CPF</p>`;
            });
    } else {
        document.getElementById('resultado').innerHTML = `<p>CPF inválido</p>`;
    }
}
