import json
from bs4 import BeautifulSoup

# Caminho para o arquivo JSON
file_path = 'clausulas.json'

html_top_content = """
<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerar Contrato</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/docx@7.1.0/build/index.min.js"></script>
    
    <!-- Estilizacao do contrato na página html equivalente ao modelo real do contrato. -->
    <style>
        * {
            margin: 0;
            padding: 0;
            font-family: 'Times New Roman', Arial, sans-serif;
            font-size: 16px;
        }

        main {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
            padding: 20px;
        }

        #buttons {
            padding: 2rem;
            display: flex;
            gap: 1rem;
        }

        #exportPDF,
        #exportDocx {
            padding: 0.5rem;
            font-weight: bold;
            font-family: monospace, sans-serif, Arial, Helvetica;
            width: 260px;
            background-color: #E6D353;
            border: 2px solid #141414;
            border-radius: 12px;
            text-transform: uppercase;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s ease, letter-spacing 0.3s ease;
        }

        button:hover {
            letter-spacing: 0.09rem;
            transform: scale(1.1);
        }

        #contrato {
            margin-top: 1rem;
            width: 210mm;
            min-height: 297mm;
            background-color: white;
            padding: 2.55cm;
            box-shadow: 0 0 10px rgba(0, 0, 0);
            border: 1px solid #ddd;
            text-align: justify;
        }

        h1 {
            text-align: center;
            font-size: 18px;
            margin-bottom: 2rem;
        }

        h2 {
            text-align: left;
            margin-bottom: 0.5rem;
            margin-top: 2rem;
        }

        p,
        ul {
            margin-bottom: 1rem;
        }

        ul {
            margin-left: 1rem;
        }

        li {
            padding: 0.5rem;
        }

        #grifar {
            background-color: yellow;
        }
    </style>
</head>

<body>
    <main>
        <!-- Botões para exportar o contrato em formato PDF ou DOCX. -->
        <section id="buttons">
            <button id="exportPDF">Exportar para PDF</button>
            <button id="exportDocx">Exportar para DOCX</button>
        </section>

        <section id="contrato">
"""

html_bottom_content = """
        </section>
    </main>

    <script>
        // Gerador de PDF sobre o conteúdo HTML usando jsPDF.
        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById('exportPDF').addEventListener("click", () => {
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF("p", "mm", "a4"); // Orientacao Portrait (Retrato), Unidade em Milimetros, Formato A4.

                const margin = 25.5; // Margem superior e lateral de 2,55cm (Equivale a margem normal no Word).
                let y = margin;      // Coordenada onde o conteúdo comecara a ser escrito.

                const contrato = document.getElementById("contrato");

                // Calcula a largura utilizável da página subtraindo as margens laterais.
                const pageWidth = pdf.internal.pageSize.getWidth() - 2 * margin;

                pdf.setFont("times", "normal");

                // Processa cada elemento dentro do HTML para convertê-lo corretamente para o PDF.
                function processElement(element) {
                    if (element.tagName === "H1") { // Elemento h1.
                        pdf.setFontSize(14);
                        pdf.setFont("times", "bold");

                        let title = element.innerText;

                        // Divide o texto para caber na largura disponível.
                        let splitTitle = pdf.splitTextToSize(title, pageWidth);
                        // Altura do texto.
                        let titleHeight = splitTitle.length * 6;

                        // Se não houver espaço suficiente na página, cria uma nova página e reseta y.
                        if (y + titleHeight > pdf.internal.pageSize.getHeight() - margin) {
                            pdf.addPage();
                            y = margin;
                        }

                        let titleWidth = pdf.getTextWidth(title);
                        
                        // Centraliza o título e move y para a próxima linha.
                        pdf.text(title, (pageWidth - titleWidth) / 2 + margin, y);
                        y += titleHeight + 5;
                    } else if (element.tagName === "H2") { // Elemento h2.
                        pdf.setFontSize(12);
                        pdf.setFont("times", "bold");

                        let title = element.innerText;
                        let splitTitle = pdf.splitTextToSize(title, pageWidth);
                        let titleHeight = splitTitle.length * 6;

                        if (y + titleHeight > pdf.internal.pageSize.getHeight() - margin) {
                            pdf.addPage();
                            y = margin;
                        }

                        pdf.text(splitTitle, margin, y);
                        y += titleHeight + 5;
                    } else if (element.tagName === "P" || element.tagName === "LI") {
                        pdf.setFontSize(12);
                        pdf.setFont("times", "normal");

                        let text = element.innerText;
                        // Divide o texto em várias linhas para caber no PDF.
                        let splitText = pdf.splitTextToSize(text, pageWidth);
                        let textHeight = splitText.length * 6;

                        if (y + textHeight > pdf.internal.pageSize.getHeight() - margin) {
                            pdf.addPage();
                            y = margin;
                        }

                        pdf.text(splitText, margin, y);
                        y += textHeight + 5;
                    } else if (element.tagName === "UL") {
                        pdf.setFontSize(12);
                        pdf.setFont("times", "normal");

                        // Para listas não ordenadas (UL), percorre cada item (LI), adicionando um ponto "•" antes do texto.
                        for (let li of element.children) {
                            let bulletText = `• ${li.innerText}`;
                            let splitBullet = pdf.splitTextToSize(bulletText, pageWidth);
                            let textHeight = splitBullet.length * 6;

                            // Se não houver espaço suficiente, adiciona uma nova página.
                            if (y + textHeight > pdf.internal.pageSize.getHeight() - margin) {
                                pdf.addPage();
                                y = margin;
                            }

                            pdf.text(splitBullet, margin, y);
                            y += textHeight + 2;
                        }
                        return;
                    }
                }

                // Percorre todos os elementos dentro de #contrato e os processa usando processElement().
                for (let el of contrato.children) {
                    processElement(el);
                }

                pdf.save("contrato.pdf");
            });
        });

        // Gerador de DOCX sobre o conteúdo HTML.
        document.getElementById("exportDocx").addEventListener("click", () => {
            if (!window.docx) {
                alert("A biblioteca docx ainda não carregou. Tente novamente.");
                return;
            }

            const { Document, Packer, Paragraph, TextRun, AlignmentType, Numbering, LevelFormat } = window.docx;
            const contrato = document.getElementById("contrato");

            // Document                → Representa o documento DOCX.
            // Packer                  → Converte o documento para Blob (formato de download).
            // Paragraph               → Representa um parágrafo no documento.
            // TextRun                 → Representa um trecho de texto dentro de um parágrafo.
            // AlignmentType           → Define alinhamento do texto (esquerda, centralizado, justificado, etc.).
            // Numbering e LevelFormat → Configuram listas numeradas.

            // children    → Armazena os elementos do documento que serão adicionados ao DOCX.
            // listCounter → Usado para numerar listas ordenadas.
            let children = [];
            let listCounter = 1;

            // Percorre todos os elementos filhos do contrato.
            // Verifica se o nó é um elemento HTML (ignorando espaços em branco e quebras de linha).
            contrato.childNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    // textRuns       → Cria um bloco de texto básico com o conteúdo do elemento.
                    // paragraphProps → Define um espaçamento padrão entre parágrafos (after: 200 = 20pt).
                    let textRuns = [new TextRun({ text: node.innerText })];
                    let paragraphProps = { spacing: { after: 200 } };

                    if (node.tagName === "H1") { // Elemento h1.
                        // Define o texto negrito e tamanho 28.
                        // Centraliza o título.
                        textRuns = [new TextRun({ text: node.innerText, bold: true, size: 28 })];
                        paragraphProps.alignment = AlignmentType.CENTER;
                    } else if (node.tagName === "H2") { // Elemento h2.
                        textRuns = [new TextRun({ text: node.innerText, bold: true, size: 24 })];
                        // Alinha à esquerda.
                        paragraphProps.alignment = AlignmentType.LEFT;
                    } else if (node.tagName === "P") { // Elemento p.
                        textRuns = [new TextRun({ text: node.innerText, size: 24 })];
                        // Justifica o texto.
                        paragraphProps.alignment = AlignmentType.JUSTIFIED;
                    } else if (node.tagName === "UL") { // Elemento ul.

                        // Para cada item da lista (LI):
                        // Cria um parágrafo com o texto do item.
                        // Para lista (UL) adiciona usa marcadores (•).
                        Array.from(node.children).forEach((li) => {
                            let listItemText = li.innerText;

                            children.push(new Paragraph({
                                children: [new TextRun({ text: listItemText, size: 24 })],
                                bullet: { level: 0 }
                            }));
                        });

                        return;
                    }

                    // Adiciona o parágrafo processado à lista de elementos (children).
                    children.push(new Paragraph({ children: textRuns, ...paragraphProps }));
                }
            });

            // Configura numeração para as listas.
            // Define os elementos processados (children) como o conteúdo do documento.
            const doc = new Document({
                numbering: {
                    config: [{
                        reference: "numbered-list",
                        levels: [{
                            level: 0,
                            format: LevelFormat.DECIMAL,
                            text: "%1.",
                            alignment: AlignmentType.LEFT,
                        }]
                    }]
                },
                sections: [{
                    properties: {},
                    children
                }]
            });

            // Packer.toBlob(doc) para converter o documento para Blob (formato que pode ser baixado).
            // Cria um link invisível <a>, define o arquivo como "contrato.docx" e simula um clique para iniciar o download.
            Packer.toBlob(doc).then(blob => {
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "contrato.docx";
                link.click();
            });
        });
    </script>
</body>

</html>
"""

def gerar_html(dados_contrato):
    
    html_contract_content = ""

    contrato = dados_contrato['dados-contrato']['contrato']
    
    nome_contrato_completo = ""
    campo_cabecalho = ""
    campo_assinaturas = ""
    clausulas_obrigatorias = ""

    if contrato == "aluguel":
        nome_contrato_completo = "Aluguel de Imóvel"

        campo_cabecalho += """
            <p>
                <strong>LOCADOR:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão],
                        portador(a) do CPF/CNPJ nº [__________], residente e domiciliado(a) na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>LOCATÁRIO:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão],
                        portador(a) do CPF/CNPJ nº [__________], residente e na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>
                    Têm entre si, de maneira justa e contratada,
                    o presente contrato de locação de imóvel,
                    que se regerá pelas cláusulas seguintes:
                </strong>
            </p>
        """

        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] – REAJUSTE DO ALUGUEL</h2>
            <p>
                O valor do aluguel será reajustado anualmente,
                com base <span id="grifar"><strong>no índice [IGP-M, IPCA, ou outro índice acordado]</strong></span>, ou,
                caso este índice se torne indisponível,
                por outro índice oficial que reflita a variação do poder de compra da moeda.
            </p>

            <h2>CLÁUSULA [XX] – OBRIGAÇÕES DO LOCADOR</h2>
            <p>O LOCADOR se compromete a:</p>
            <ul>
                <li>Garantir ao LOCATÁRIO o uso pacífico do imóvel durante o prazo da locação;</li>
                <li>
                    Realizar os reparos necessários nas instalações do imóvel,
                    salvo danos causados pelo uso inadequado;
                </li>
                <li>Entregar o imóvel em condições de uso e habitabilidade, conforme acordado.</li>
            </ul>

            <h2>CLÁUSULA [XX] – OBRIGAÇÕES DO LOCATÁRIO</h2>
            <p>O LOCATÁRIO se compromete a:</p>
            <ul>
                <li>Pagar pontualmente o aluguel e encargos da locação, conforme estabelecido na cláusula 3;</li>
                <li>Conservar o imóvel, realizando pequenos reparos necessários em decorrência de uso inadequado;</li>
                <li>Não sublocar, ceder ou emprestar o imóvel a terceiros sem a expressa autorização do LOCADOR.</li>
            </ul>

            <h2>CLÁUSULA [XX] - DA CONSERVAÇÃO, REFORMAS E BENFEITORIAS NECESSÁRIAS</h2>
            <ul>
                <li>Ao LOCATÁRIO recai a responsabilidade por zelar pela conservação, limpeza e segurança do imóvel.</li>
                <li>
                    As benfeitorias necessárias introduzidas pelo LOCATÁRIO,
                    ainda que não autorizadas pelo LOCADOR, bem como as úteis, desde que autorizadas,
                    serão indenizáveis e permitem o exercício do direito de retenção.
                    As benfeitorias voluptuárias não serão indenizáveis, podendo ser levantadas pelo LOCATÁRIO, 
                    finda a locação, desde que sua retirada não afete a estrutura e a substância do imóvel.
                </li>
                <li>
                    O LOCATÁRIO está obrigado a devolver o imóvel em perfeitas condições de limpeza,
                    conservação e pintura, quando finda ou rescindida esta avença,
                    conforme constante no termo de vistoria em anexo.
                </li>
                <li>
                    O LOCATÁRIO não poderá realizar obras que alterem ou modifiquem a estrutura do imóvel locado,
                    sem prévia autorização por escrito da LOCADORA.
                    No caso de prévia autorização, as obras serão incorporadas ao imóvel,
                    sem que caiba ao LOCATÁRIO qualquer indenização pelas obras ou retenção por benfeitorias.
                </li>
            </ul>

            <h2>CLÁUSULA [XX] – VISTORIA DO IMÓVEL</h2>
            <p>
                As partes realizarão, na data da assinatura deste contrato, uma vistoria detalhada do imóvel,
                que será documentada em relatório, com fotos e descrição das condições do imóvel.
                O LOCATÁRIO se compromete a devolver o imóvel nas mesmas condições, 
                salvo o desgaste natural decorrente do uso.
            </p>
        """
        campo_assinaturas += """
        <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Locador</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Locatário</strong></p>
        """
    elif contrato == "cessao-direitos":
        nome_contrato_completo = "Cessão de Direitos sobre Imóvel"

        campo_cabecalho += """
            <p><strong>Pelo presente instrumento particular, as partes abaixo identificadas:</strong></p>

            <p>
                <strong>CEDENTE:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo do cedente], [qualificação completa], residente e domiciliado à [endereço completo], 
                        portador(a) do CPF nº [número do CPF] e RG nº [número do RG].
                    </strong>
                </span>
            </p>

            <p>
                <strong>CESSIONÁRIO:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo do cessionário], [qualificação completa], residente e domiciliado à [endereço completo], 
                        portador(a) do CPF nº [número do CPF] e RG nº [número do RG].
                    </strong>
                </span>
            </p>

            <p><strong>Têm entre si, de forma justa e contratada, o seguinte:</strong></p>
        """
        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] - OBRIGAÇÕES DAS PARTES</h2>
            <p>Obrigações do CEDENTE:</p>
            <ul>
                <li>
                    O CEDENTE se compromete a transferir todos os direitos sobre o imóvel ao CESSIONÁRIO, 
                    garantindo que o imóvel não possui ônus ou dívidas que possam comprometer a cessão. 
                </li>
                <li>
                    O CEDENTE se compromete a fornecer ao CESSIONÁRIO toda a documentação necessária à regularização e formalização da cessão, 
                    caso seja necessário.
                </li>
            </ul>
            <p>Obrigações do CESSIONÁRIO:</p>
            <ul>
                <li>
                    O CESSIONÁRIO se compromete a cumprir as obrigações assumidas no contrato originário, 
                    como pagamento de parcelas, tributos ou outras responsabilidades associadas ao imóvel. 
                </li>
                <li>
                    O CESSIONÁRIO se compromete a respeitar a finalidade para a qual os direitos foram cedidos e a devolução do imóvel, 
                    caso seja o caso, nas condições previstas.
                </li>
            </ul>

            <h2>CLÁUSULA [XX] - TRANSFERÊNCIA DE DOCUMENTOS</h2>
            <p>
                O CEDENTE compromete-se a entregar ao CESSIONÁRIO todos os documentos relacionados ao imóvel, 
                como a escritura, o contrato de compra e venda, matrícula atualizada, 
                e quaisquer outros documentos necessários à transferência dos direitos.
            </p>

            <h2>CLÁUSULA [XX] - IMPOSIÇÃO DE CESSÃO A TERCEIROS</h2>
            <p>
                O CESSIONÁRIO não poderá ceder os direitos aqui transferidos a terceiros sem a prévia e expressa autorização do CEDENTE.
            </p>
        """
        campo_assinaturas += """
            <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Cedente</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Cessionário</strong></p>
        """
    elif contrato == "comodato":
        nome_contrato_completo = "Comodato de Imóvel"

        campo_cabecalho += """
            <p><strong>Pelo presente instrumento particular de contrato de comodato, as partes abaixo identificadas:</strong></p>

            <p>
                <strong>COMODANTE:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo], [qualificação completa], residente e domiciliado à [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>COMODATÁRIO:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo], [qualificação completa], residente e domiciliado à [endereço completo].
                    </strong>
                </span>
            </p>

            <p><strong>Têm entre si, justas e contratadas, as seguintes cláusulas e condições:</strong></p>
        """
        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] - OBRIGAÇÕES DO COMODATÁRIO</h2>
            <p>O COMODATÁRIO se compromete a:</p>
            <ul>
                <li>Utilizar o imóvel exclusivamente para a finalidade estabelecida neste contrato;</li>
                <li>Conservar o imóvel, mantendo-o em bom estado de uso e habitabilidade;</li>
                <li>Realizar reparos necessários ao imóvel, caso seja responsável por danos causados por seu uso;</li>
                <li>Devolver o imóvel ao COMODANTE no prazo acordado, em perfeitas condições de uso, salvo desgastes naturais do tempo.</li>
            </ul>

            <h2>CLÁUSULA [XX] - OBRIGAÇÕES DO COMODANTE</h2>
            <p>O COMODANTE se compromete a:</p>
            <ul>
                <li>Entregar o imóvel ao COMODATÁRIO em boas condições de uso e habitabilidade;</li>
                <li>Garantir o uso pacífico do imóvel durante o prazo do contrato, não permitindo que terceiros impeçam o uso regular do imóvel.</li>
            </ul>

            <h2>CLÁUSULA [XX] - MANUTENÇÃO E REPAROS</h2>
            <p>
                O COMODATÁRIO será responsável pelos reparos decorrentes de seu uso e pela manutenção do imóvel, 
                exceto nos casos de deterioração natural do imóvel.
            </p>
            <p>O COMODANTE poderá, a qualquer momento, solicitar vistorias no imóvel para verificar suas condições.</p>

            <h2>CLÁUSULA [XX] - CESSÃO E SUBLOCAÇÃO</h2>
            <p>
                O COMODATÁRIO não poderá ceder, sublocar ou transferir os direitos do presente contrato a terceiros, 
                total ou parcialmente, sem o consentimento prévio e por escrito do COMODANTE.
            </p>
        """
        campo_assinaturas += """
            <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Comodante</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Comodatário</strong></p>
        """
    elif contrato == "compra-venda":
        nome_contrato_completo = "Compra e Venda de Imóvel"

        campo_cabecalho += """
            <p><strong>Pelo presente instrumento particular, de um lado:</strong></p>

            <p>
                <strong>VENDEDOR:</strong> 
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão], 
                        portador(a) do CPF/CNPJ nº [__________], residente e domiciliado(a) na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>COMPRADOR:</strong> 
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão], 
                        portador(a) do CPF/CNPJ nº [__________], residente e domiciliado(a) na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>
                    Têm entre si, de maneira justa e contratada, o presente contrato de compra e venda, 
                    que se regerá pelas cláusulas seguintes:
                </strong>
            </p>
        """
        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] – TRANSFERÊNCIA DE PROPRIEDADE</h2>
            <p>
                A transferência da propriedade do bem ocorrerá após o pagamento integral 
                do valor acordado e a formalização da entrega do bem. 
                O VENDEDOR se compromete a fornecer todos os documentos necessários 
                para a transferência de titularidade do bem ao COMPRADOR.
            </p>

            <h2>CLÁUSULA [XX] – RESPONSABILIDADE PELOS DÉBITOS</h2>
            <p>
                O VENDEDOR declara que o bem encontra-se livre de qualquer ônus, gravame ou dívida, 
                respondendo integralmente pela quitação de débitos anteriores à data de entrega, caso existam.
            </p>
            
            <h2>CLÁUSULA [XX] - DAS DESPESAS</h2>
            <p>
                Todas as despesas de registro do presente contrato e da futura escritura com todas as taxas e impostos devidos, 
                correrão por conta exclusiva do COMPRADOR em especial, se for o caso, as abaixo relacionadas:
            </p>
            <ul> 
                <li>Imposto de transmissão (ITBI);</li>
                <li>Emolumentos e custos de Registros de imóveis;</li>
                <li>Custos e emolumentos do Cartório de Notas;</li>
                <li>
                    Despesas indispensáveis à instalação, 
                    funcionamento regulamentação do condomínio na proporção das respectivas frações ideais do terreno.
                </li>
            </ul>

            <h2>CLÁUSULA [XX] – RISCO E RESPONSABILIDADE</h2>
            <p>
                A partir da entrega do bem, o risco sobre o bem será transferido para o COMPRADOR, 
                o qual assume a responsabilidade por quaisquer danos ou perdas que possam ocorrer após essa entrega.
            </p>
        """
        campo_assinaturas += """
            <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Vendedor</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Comprador</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura da Testemunha 1</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura da Testemunha 2</strong></p>
        """
    elif contrato == "permuta":
        nome_contrato_completo = "Permuta de Imóvel"

        campo_cabecalho += """
            <p>
                <span id="grifar">
                    <strong>
                        [NOME COMPLETO DO PERMUTANTE 1], [qualificação completa], residente e domiciliado à [endereço completo], 
                        doravante denominado PERMUTANTE 1.
                    </strong>
                </span>
            </p>

            <p>
                <span id="grifar">
                    <strong>
                        [NOME COMPLETO DO PERMUTANTE 2], [qualificação completa], residente e domiciliado à [endereço completo],
                        doravante denominado PERMUTANTE 2.
                    </strong>
                </span>
            </p>

            <p>
                <strong>Têm entre si, justas e contratadas, as seguintes cláusulas e condições:</strong>
            </p>
        """
        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] - COMPLEMENTO EM DINHEIRO (SE APLICÁVEL)</h2>
            <p>
                Caso um dos imóveis tenha valor superior ao outro, 
                a parte que receber o imóvel de menor valor pagará à outra a diferença, 
                no valor de <span id="grifar"><strong>R$ [valor da diferença]</strong></span>, 
                em <span id="grifar"><strong>[número de parcelas]</strong></span>, 
                com vencimento da primeira parcela em <span id="grifar"><strong>[data]</strong></span>, 
                podendo ser paga por meio de <span id="grifar"><strong>[forma de pagamento acordada]</strong></span>.
            </p>

            <h2>CLÁUSULA [XX] - OBRIGAÇÕES DAS PARTES</h2>
            <p>As partes se obrigam a:</p>
            <ul>
                <li>Entregar os imóveis livres de qualquer ônus, gravame, dívida ou litígios;</li>
                <li>
                    Apresentar toda a documentação necessária para a formalização da permuta, 
                    incluindo certidões negativas e escritura pública, se necessário;
                </li>
                <li>Cumprir as obrigações fiscais e tributárias relativas à permuta até a data da efetiva troca.</li>
            </ul>

            <h2>CLÁUSULA [XX] - CONDIÇÕES DO IMÓVEL</h2>
            <p>
                As partes declaram que os imóveis estão em boas condições de uso e gozo, 
                conforme vistoria realizada na data da assinatura deste contrato.
            </p>
            <p>
                Caso uma das partes constate problemas estruturais ou outras condições que afetem o valor do imóvel após a assinatura, 
                poderá exigir a reparação ou compensação da outra parte.
            </p>
        """

        campo_assinaturas += """
            <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Permutante 1</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Permutante 2</strong></p>
        """
    elif contrato == "prestacao-servicos":
        nome_contrato_completo = "Prestação de Serviços"

        campo_cabecalho += """
            <p><strong>Pelo presente instrumento particular, as partes abaixo assinadas:</strong></p>

            <p>
                <strong>CONTRATANTE:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão],
                        portador(a) do CPF/CNPJ nº [__________], residente e domiciliado(a) na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>CONTRATADO:</strong>
                <span id="grifar">
                    <strong>
                        [Nome completo ou razão social], [Nacionalidade], [Estado civil], [Profissão],
                        portador(a) do CPF/CNPJ nº [__________], residente e domiciliado(a) na [endereço completo].
                    </strong>
                </span>
            </p>

            <p>
                <strong>
                    Têm entre si, de maneira justa e contratada, 
                    o presente contrato de prestação de serviços, que se regerá pelas cláusulas seguintes:
                </strong>
            </p>
        """
        clausulas_obrigatorias += """
            <h2>CLÁUSULA [XX] – OBRIGAÇÕES DO CONTRATADO</h2>
            <p>O Contratado se compromete a:</p>
            <ul>
                <li>Prestar os serviços de forma diligente e em conformidade com os padrões técnicos exigidos;</li>
                <li>Cumprir os prazos estabelecidos para a execução dos serviços;</li>
                <li>Fornecer relatórios de andamento quando solicitado pelo Contratante;</li>
                <li>Garantir a confidencialidade das informações fornecidas pelo Contratante, exceto quando houver obrigação legal de divulgação.</li>
            </ul>

            <h2>CLÁUSULA [XX] – OBRIGAÇÕES DO CONTRATANTE</h2>
            <p>O Contratante se compromete a:</p>
            <ul>
                <li>Fornecer todas as informações e documentos necessários para a execução dos serviços;</li>
                <li>Efetuar o pagamento conforme o acordado na cláusula 3;</li>
                <li>Cooperar com o Contratado para garantir o andamento dos serviços de forma eficiente.</li>
            </ul>

            <h2>CLÁUSULA [XX] – CONFIDENCIALIDADE</h2>
            <p>
                As partes se obrigam a manter sigilo sobre todas as informações 
                e documentos fornecidos durante a execução dos serviços, 
                não podendo divulgá-los sem o consentimento prévio da outra parte, salvo por exigência legal.
            </p>

            <h2>CLÁUSULA [XX] – PROPRIEDADE INTELECTUAL</h2>
            <p>
                Os direitos de propriedade intelectual sobre os produtos 
                ou resultados gerados durante a execução dos serviços serão 
                <span id="grifar"><strong>[detalhar se pertencem ao Contratante, ao Contratado ou se serão compartilhados].</strong></span>
            </p>
        """
        campo_assinaturas += """
            <p style="margin-top: 10rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Local e Data</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Contratado</strong></p>
            <p style="margin-top: 5rem; text-align: center;">__________________________________</p>
            <p style="text-align: center;"><strong>Assinatura do Contratante</strong></p>
        """

    html_contract_content += f"<h1>CONTRATO DE {nome_contrato_completo.upper()}</h1>\n" + campo_cabecalho

    # Abrindo e carregando o arquivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
        data_clausulas = data["clausulas"]

    # Loop para processar cada cláusula no contrato
    for clausula_contrato in dados_contrato["dados-contrato"]["clausulas"]:
        clausula_nome = clausula_contrato["nome"]
        itens_incluidos = clausula_contrato["itens"]

        # Encontrar a cláusula correspondente no arquivo de cláusulas
        clausula_encontrada = next((clausula for clausula in data_clausulas if clausula["id"] == clausula_nome), None)

        if clausula_encontrada:
            # Adiciona o título da cláusula no HTML
            html_contract_content += f"<h2>{clausula_encontrada['titulo']}</h2>\n"

            list_itens = ""

            if "completo" in itens_incluidos:
                # Se "completo", adiciona todos os itens da cláusula
                for chave, valor in clausula_encontrada.items():
                    if chave.startswith("item"):
                        html_contract_content += f"<p>{valor}</p>\n"
                    elif chave.startswith("li"):
                        list_itens += f"<li>{valor}</li>\n"

                if list_itens:
                    html_contract_content += "<ul>\n" + list_itens + "</ul>\n"
            else:
                # Caso contrário, só inclui os itens listados em "itens"
                for item in itens_incluidos:
                    if item in clausula_encontrada:
                        html_contract_content += f"<p>{clausula_encontrada[item]}</p>\n"
        else:
            print(f"Cláusula {clausula_nome} não encontrada.")


    full_html = html_top_content +  html_contract_content + clausulas_obrigatorias + campo_assinaturas + html_bottom_content

    html_formatado = formatar_html(full_html)

    with open("contrato_gerado.html", "w", encoding="utf-8") as file:
        file.write(html_formatado)
        
    return html_formatado


def formatar_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()

