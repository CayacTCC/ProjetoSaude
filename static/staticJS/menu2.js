document.addEventListener('DOMContentLoaded', () => {
    // Interatividade básica para menus em dispositivos móveis
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        link.addEventListener('click', (e) => {
            if (window.innerWidth <= 850) {
                e.preventDefault();
                dropdown.classList.toggle('open');
            }
        });
    });

    // ==========================================
    // PREENCHIMENTO AUTOMÁTICO DE ENDEREÇO (VIA CEP)
    // ==========================================
    const inputCep = document.getElementById('cep');

    if (inputCep) {
        inputCep.addEventListener('blur', (e) => {
            let cep = e.target.value.replace(/\D/g, ''); // Remove traços ou pontos

            if (cep.length === 8) {
                const url = `https://viacep.com.br/ws/${cep}/json/`;

                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            // Preenche os campos do formulário automaticamente
                            document.getElementById('rua').value = data.logradouro || '';
                            document.getElementById('bairro').value = data.bairro || '';
                            document.getElementById('cidade').value = data.localidade || '';
                            document.getElementById('uf').value = data.uf || '';
                            
                            // Joga o foco direto para o campo número
                            document.getElementById('numero').focus();
                        } else {
                            alert('CEP não encontrado na base de dados.');
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao consultar a API ViaCEP:', error);
                        alert('Não foi possível buscar o CEP. Verifique sua conexão.');
                    });
            }
        });
    }

    // Ação opcional ao enviar o formulário de cadastro
    const formCadastro = document.getElementById('form-cadastro');
    if (formCadastro) {
        formCadastro.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Dados de cadastro salvos com sucesso!');
        });
    }
});