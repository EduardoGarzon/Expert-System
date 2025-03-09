function coletarDadosFormulario() {
    const form = document.getElementById("contractForm");
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });
    return jsonData;
}

function enviarFormulario() {
    let selects = document.querySelectorAll("#contractForm select");
    let todasNao = true;

    selects.forEach(select => {
        if (select.value !== "nao" && select.value !== "Responder") {
            todasNao = false;
        }
    });

    if (todasNao) {
        alert("Respostas insuficientes para gerar o modelo de contrato!");
        return;
    }
    else {
        const jsonData = coletarDadosFormulario();

        fetch("http://127.0.0.1:5000/gerar-contrato", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData)
        })
            .then(response => response.json())
            .then(data => {
                let iframe = document.getElementById('contratoFrame').contentWindow.document;
                iframe.open();
                iframe.write(data);
                iframe.close();

                let iframeWindow = document.getElementById('contratoFrame');
                iframeWindow.style.display = "block";
            })
            .catch(error => console.error("Erro:", error));
    }
}

function baixarJSON() {
    const jsonData = coletarDadosFormulario();
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "dados_contrato.json";
    link.click();
}