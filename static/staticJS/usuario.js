document.addEventListener('DOMContentLoaded', () => {
    // Interatividade básica para menus em dispositivos móveis
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        if (link) {
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 850) {
                    e.preventDefault();
                    dropdown.classList.toggle('open');
                }
            });
        }
    });

    // ==========================================
    // PREENCHIMENTO AUTOMÁTICO DE ENDEREÇO (VIA CEP)
    // ==========================================
    const inputCep = document.getElementById('cep');
    const inputRua = document.getElementById('rua');
    const inputBairro = document.getElementById('bairro');
    const inputCidade = document.getElementById('cidade');
    const inputUf = document.getElementById('uf');
    const inputNumero = document.getElementById('numero');

    let ultimoCepBuscado = '';

    function formatarCep(valor) {
        const digitos = valor.replace(/\D/g, '').slice(0, 8);
        if (digitos.length > 5) {
            return `${digitos.slice(0, 5)}-${digitos.slice(5)}`;
        }
        return digitos;
    }

    function buscarViaCep(cepLimpo) {
        if (cepLimpo.length !== 8 || cepLimpo === ultimoCepBuscado) {
            return;
        }
        ultimoCepBuscado = cepLimpo;

        const url = `https://viacep.com.br/ws/${cepLimpo}/json/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    if (inputRua) inputRua.value = data.logradouro || '';
                    if (inputBairro) inputBairro.value = data.bairro || '';
                    if (inputCidade) inputCidade.value = data.localidade || '';
                    if (inputUf) inputUf.value = data.uf || '';
                    if (inputNumero) inputNumero.focus();
                } else {
                    alert('CEP não encontrado na base de dados.');
                }
            })
            .catch(error => {
                console.error('Erro ao consultar a API ViaCEP:', error);
                alert('Não foi possível buscar o CEP. Verifique sua conexão.');
            });
    }

    if (inputCep) {
        if (inputCep.value) {
            inputCep.value = formatarCep(inputCep.value);
        }

        const tratarCep = (e) => {
            const cepFormatado = formatarCep(e.target.value);
            e.target.value = cepFormatado;

            const cepLimpo = cepFormatado.replace(/\D/g, '');
            if (cepLimpo.length === 8) {
                buscarViaCep(cepLimpo);
            }
        };

        inputCep.addEventListener('input', tratarCep);
        inputCep.addEventListener('blur', tratarCep);
    }
});