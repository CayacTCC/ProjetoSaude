(function () {
    const DOMINIOS_EMAIL_VALIDOS = new Set([
        "gmail.com",
        "gmail.com.br",
        "googlemail.com",
        "outlook.com",
        "outlook.com.br",
        "hotmail.com",
        "hotmail.com.br",
        "live.com",
        "live.com.br",
        "msn.com",
        "msn.com.br",
        "yahoo.com",
        "yahoo.com.br",
        "ymail.com",
        "rocketmail.com",
        "icloud.com",
        "me.com",
        "mac.com",
        "uol.com.br",
        "bol.com.br",
        "terra.com.br",
        "ig.com.br",
        "globo.com",
        "globomail.com",
        "r7.com",
        "oi.com.br",
        "zipmail.com.br",
        "pop.com.br",
        "proton.me",
        "protonmail.com",
        "zoho.com",
        "zoho.com.br",
        "aol.com",
        "gmx.com",
        "gmx.de",
        "mail.com",
        "yandex.com",
        "fastmail.com"
    ]);

    function formatarCPF(cpfTexto) {
        const digitos = String(cpfTexto || "").replace(/\D/g, "").slice(0, 11);

        if (digitos.length <= 3) {
            return digitos;
        }
        if (digitos.length <= 6) {
            return digitos.replace(/(\d{3})(\d+)/, "$1.$2");
        }
        if (digitos.length <= 9) {
            return digitos.replace(/(\d{3})(\d{3})(\d+)/, "$1.$2.$3");
        }
        return digitos.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, "$1.$2.$3-$4");
    }

    function calcularDigitoVerificador(digitos, pesoInicial) {
        let soma = 0;
        for (let i = 0; i < digitos.length; i++) {
            soma += digitos[i] * (pesoInicial - i);
        }
        const resto = (soma * 10) % 11;
        return (resto === 10 || resto === 11) ? 0 : resto;
    }

    function validarCPF(cpfTexto) {
        const cpfLimpo = String(cpfTexto || "").replace(/\D/g, "");
        if (cpfLimpo.length !== 11) return false;
        if (/^(\d)\1{10}$/.test(cpfLimpo)) return false;

        const nums = cpfLimpo.split("").map(Number);
        const d1 = calcularDigitoVerificador(nums.slice(0, 9), 10);
        if (d1 !== nums[9]) return false;

        const d2 = calcularDigitoVerificador(nums.slice(0, 10), 11);
        if (d2 !== nums[10]) return false;

        return true;
    }

    function validarEmail(emailTexto) {
        const email = String(emailTexto || "").trim().toLowerCase();
        if (!email || email.includes(" ")) return false;

        const partes = email.split("@");
        if (partes.length !== 2) return false;

        const usuario = partes[0];
        const dominio = partes[1];
        if (!usuario || !dominio) return false;

        if (!/^[a-z0-9._%+-]+$/.test(usuario)) return false;
        if (usuario.startsWith(".") || usuario.endsWith(".") || usuario.includes("..")) return false;
        if (dominio.startsWith(".") || dominio.endsWith(".") || dominio.includes("..")) return false;

        return DOMINIOS_EMAIL_VALIDOS.has(dominio);
    }

    function checarCpf() {
        const inputCpf = document.getElementById("cpf");
        const spanCpf = document.getElementById("erro-cpf");
        const ok = validarCPF(inputCpf ? inputCpf.value : "");
        if (spanCpf) {
            spanCpf.textContent = ok ? "" : "CPF inválido. Confira os números digitados.";
        }
        return ok;
    }

    function checarEmail() {
        const inputEmail = document.getElementById("email");
        const spanEmail = document.getElementById("erro-email");
        const ok = validarEmail(inputEmail ? inputEmail.value : "");
        if (spanEmail) {
            spanEmail.textContent = ok
                ? ""
                : "E-mail inválido. Use um endereço válido (ex: @gmail.com, @outlook.com, @yahoo.com, @icloud.com).";
        }
        return ok;
    }

    function validarTudo(event) {
        const inputCpf = document.getElementById("cpf");
        const inputEmail = document.getElementById("email");
        const nome = document.getElementById("nome") ? document.getElementById("nome").value.trim() : "";
        const senha = document.getElementById("senha") ? document.getElementById("senha").value : "";

        const cpfValidoOk = checarCpf();
        const emailValidoOk = checarEmail();

        if (!cpfValidoOk || !emailValidoOk || !nome || !senha) {
            if (event) {
                event.preventDefault();
                event.stopPropagation();
                if (typeof event.stopImmediatePropagation === "function") {
                    event.stopImmediatePropagation();
                }
            }
            if (!cpfValidoOk && inputCpf) {
                inputCpf.focus();
            } else if (!emailValidoOk && inputEmail) {
                inputEmail.focus();
            }
            return false;
        }

        return true;
    }

    document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("formCadastro");
        const inputCpf = document.getElementById("cpf");
        const inputEmail = document.getElementById("email");

        if (form) {
            form.addEventListener("submit", validarTudo, true);
        }

        if (inputCpf) {
            inputCpf.addEventListener("input", function () {
                inputCpf.value = formatarCPF(inputCpf.value);
                const spanCpf = document.getElementById("erro-cpf");
                if (spanCpf && spanCpf.textContent !== "") checarCpf();
            });

            inputCpf.addEventListener("blur", function () {
                inputCpf.value = formatarCPF(inputCpf.value);
                if (inputCpf.value.trim() !== "") checarCpf();
            });
        }

        if (inputEmail) {
            inputEmail.addEventListener("blur", function () {
                if (inputEmail.value.trim() !== "") checarEmail();
            });
            inputEmail.addEventListener("input", function () {
                const spanEmail = document.getElementById("erro-email");
                if (spanEmail && spanEmail.textContent !== "") checarEmail();
            });
        }
    });
})();