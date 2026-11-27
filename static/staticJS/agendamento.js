document.addEventListener('DOMContentLoaded', function () {
    var selectTipo = document.getElementById('tipo_atendimento');
    var selectCidade = document.getElementById('cidade_select');
    var campoHospital = document.getElementById('hospital_id');
    var selectExame = document.getElementById('exame_id');

    var boxDescricao = document.getElementById('exame-descricao-box');
    var tituloDescricao = document.getElementById('exame-descricao-titulo');
    var textoDescricao = document.getElementById('exame-descricao-texto');

    if (!campoHospital || !selectExame) return;

    var urlHospitais = campoHospital.dataset.urlHospitais;
    var urlExamesTemplate = campoHospital.dataset.urlExamesBase;

    function atualizarDescricaoExame() {
        if (!boxDescricao || !tituloDescricao || !textoDescricao) return;

        var opcaoSelecionada = selectExame.options[selectExame.selectedIndex];
        var descricao = opcaoSelecionada && opcaoSelecionada.dataset.descricao
            ? opcaoSelecionada.dataset.descricao.trim()
            : '';

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

    function resetarExames(textoPadrao, habilitar) {
        if (textoPadrao === undefined) textoPadrao = 'Selecione o hospital primeiro...';
        if (habilitar === undefined) habilitar = false;

        selectExame.innerHTML = '<option value="">' + textoPadrao + '</option>';
        selectExame.disabled = !habilitar;
        atualizarDescricaoExame();
    }

    function resetarHospitais(textoPadrao) {
        if (textoPadrao === undefined) textoPadrao = 'Selecione a cidade primeiro...';
        if (campoHospital.tagName !== 'SELECT') return;

        campoHospital.innerHTML = '<option value="">' + textoPadrao + '</option>';
        campoHospital.disabled = true;
    }

    function carregarExames(hospitalId) {
        if (!hospitalId) {
            resetarExames('Selecione o hospital primeiro...', false);
            return;
        }

        if (!urlExamesTemplate) {
            resetarExames('Erro ao carregar exames', false);
            return;
        }

        resetarExames('Carregando exames...', false);
        var urlExames = urlExamesTemplate.replace('/0/', '/' + hospitalId + '/');

        fetch(urlExames)
            .then(function (res) {
                if (!res.ok) throw new Error('HTTP ' + res.status);
                return res.json();
            })
            .then(function (data) {
                if (data.exames && data.exames.length > 0) {
                    selectExame.innerHTML = '<option value="">Selecione um exame...</option>';
                    data.exames.forEach(function (exame) {
                        var opt = document.createElement('option');
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
            .catch(function (err) {
                console.error('Erro ao buscar exames:', err);
                resetarExames('Erro ao carregar exames', false);
            });
    }

    function carregarHospitais(cidade) {
        resetarExames('Selecione o hospital primeiro...', false);

        if (!cidade) {
            resetarHospitais('Selecione a cidade primeiro...');
            return;
        }

        if (!urlHospitais) {
            resetarHospitais('URL de hospitais não configurada');
            return;
        }

        var tipoAtendimento = selectTipo ? selectTipo.value : '';
        resetarHospitais('Carregando hospitais...');

        var params = new URLSearchParams({
            cidade: cidade,
            tipo_atendimento: tipoAtendimento
        });

        fetch(urlHospitais + '?' + params.toString())
            .then(function (res) {
                if (!res.ok) throw new Error('HTTP ' + res.status);
                return res.json();
            })
            .then(function (data) {
                campoHospital.innerHTML = '<option value="">Selecione um hospital...</option>';
                if (data.hospitais && data.hospitais.length > 0) {
                    data.hospitais.forEach(function (hosp) {
                        var opt = document.createElement('option');
                        opt.value = hosp.id;
                        opt.textContent = hosp.nome;
                        campoHospital.appendChild(opt);
                    });
                    campoHospital.disabled = false;
                } else {
                    resetarHospitais('Nenhum hospital disponível para esse filtro');
                }
            })
            .catch(function (err) {
                console.error('Erro ao buscar hospitais:', err);
                resetarHospitais('Erro ao carregar hospitais');
            });
    }

    if (selectTipo) {
        selectTipo.addEventListener('change', function () {
            if (selectCidade && selectCidade.value) {
                carregarHospitais(selectCidade.value);
            } else {
                resetarHospitais('Selecione a cidade primeiro...');
                resetarExames('Selecione o hospital primeiro...', false);
            }
        });
    }

    if (selectCidade) {
        selectCidade.addEventListener('change', function (e) {
            carregarHospitais(e.target.value);
        });
    }

    if (campoHospital.tagName === 'SELECT') {
        campoHospital.addEventListener('change', function (e) {
            carregarExames(e.target.value);
        });
    } else if (campoHospital.value) {
        carregarExames(campoHospital.value);
    }

    selectExame.addEventListener('change', atualizarDescricaoExame);
});