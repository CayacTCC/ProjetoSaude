document.addEventListener('DOMContentLoaded', () => {
    const selectTipo = document.getElementById('tipo_atendimento');
    const selectCidade = document.getElementById('cidade_select');
    const campoHospital = document.getElementById('hospital_id');
    const selectExame = document.getElementById('exame_id');

    const boxDescricao = document.getElementById('exame-descricao-box');
    const tituloDescricao = document.getElementById('exame-descricao-titulo');
    const textoDescricao = document.getElementById('exame-descricao-texto');

    if (!campoHospital || !selectExame) return;

    const urlHospitais = campoHospital.dataset.urlHospitais;
    const urlExamesTemplate = campoHospital.dataset.urlExamesBase;

    function atualizarDescricaoExame() {
        if (!boxDescricao || !tituloDescricao || !textoDescricao) return;

        const opcaoSelecionada = selectExame.options[selectExame.selectedIndex];
        const descricao = opcaoSelecionada ? (opcaoSelecionada.dataset.descricao || '').trim() : '';

        if (opcaoSelecionada && opcaoSelecionada.value && descricao) {
            tituloDescricao.textContent = opcaoSelecionada.textContent;
            textoDescricao.textContent = descricao;
            boxDescricao.style.display = 'block';
        } else {
            tituloDescricao.textContent = '';
            textoDescricao.textContent = '';
            boxDescricao.style.display = 'none';
        }
    }

    function resetarExames(textoPadrao = 'Selecione um hospital primeiro...', habilitar = false) {
        selectExame.innerHTML = `<option value="">${textoPadrao}</option>`;
        selectExame.disabled = !habilitar;
        atualizarDescricaoExame();
    }

    function resetarHospitais(textoPadrao = 'Selecione uma cidade primeiro...') {
        if (campoHospital.tagName !== 'SELECT') return;
        campoHospital.innerHTML = `<option value="">${textoPadrao}</option>`;
        campoHospital.disabled = true;
    }

    function carregarExames(hospitalId) {
        if (!hospitalId) {
            resetarExames('Selecione um hospital primeiro...', false);
            return;
        }

        if (!urlExamesTemplate) {
            resetarExames('Erro ao carregar exames', false);
            return;
        }

        resetarExames('Carregando exames...', false);
        const urlExames = urlExamesTemplate.replace('/0/', `/${hospitalId}/`);

        fetch(urlExames)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                if (data.exames && data.exames.length > 0) {
                    selectExame.innerHTML = '<option value="">Selecione um exame...</option>';
                    data.exames.forEach(exame => {
                        const opt = document.createElement('option');
                        opt.value = exame.id;
                        opt.textContent = exame.nome;
                        opt.dataset.descricao = exame.descricao || '';
                        selectExame.appendChild(opt);
                    });
                    selectExame.disabled = false;
                } else {
                    resetarExames('Nenhum exame cadastrado neste hospital', false);
                }
                atualizarDescricaoExame();
            })
            .catch(err => {
                console.error('Erro ao buscar exames:', err);
                resetarExames('Erro ao carregar exames', false);
            });
    }

    function carregarHospitais(cidade) {
        resetarExames('Selecione um hospital primeiro...', false);

        if (!cidade) {
            resetarHospitais('Selecione uma cidade primeiro...');
            return;
        }

        if (!urlHospitais) {
            resetarHospitais('URL de hospitais não configurada');
            return;
        }

        const tipoAtendimento = selectTipo ? selectTipo.value : '';
        resetarHospitais('Carregando hospitais...');

        const params = new URLSearchParams({
            cidade: cidade,
            tipo_atendimento: tipoAtendimento
        });

        fetch(`${urlHospitais}?${params.toString()}`)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                campoHospital.innerHTML = '<option value="">Selecione um hospital...</option>';
                if (data.hospitais && data.hospitais.length > 0) {
                    data.hospitais.forEach(hosp => {
                        const opt = document.createElement('option');
                        opt.value = hosp.id;
                        opt.textContent = hosp.nome;
                        campoHospital.appendChild(opt);
                    });
                    campoHospital.disabled = false;
                } else {
                    resetarHospitais('Nenhum hospital disponível para esse filtro');
                }
            })
            .catch(err => {
                console.error('Erro ao buscar hospitais:', err);
                resetarHospitais('Erro ao carregar hospitais');
            });
    }

    if (selectTipo) {
        selectTipo.addEventListener('change', () => {
            if (selectCidade && selectCidade.value) {
                carregarHospitais(selectCidade.value);
            }
        });
    }

    if (selectCidade) {
        selectCidade.addEventListener('change', (e) => {
            carregarHospitais(e.target.value);
        });
    }

    if (campoHospital.tagName === 'SELECT') {
        campoHospital.addEventListener('change', (e) => {
            carregarExames(e.target.value);
        });
    } else if (campoHospital.value) {
        carregarExames(campoHospital.value);
    }

    selectExame.addEventListener('change', atualizarDescricaoExame);
});