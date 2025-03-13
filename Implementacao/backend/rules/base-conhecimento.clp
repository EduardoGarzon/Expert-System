; Luiz Eduardo Garzon
; Pedro Henrique Berti
; Kawan Oliveira
; Weberson Leite

;Definindo estrutura para o contrato.
;Usando deftemplate para definir fatos com múltiplos campos.
(deftemplate contrato
    (slot tipo-contrato)
    (slot objetivo-especifico)
    (slot partes-definidas)
    (slot tempo-duracao)
    (slot existe-pagamento)
    (slot penalidade-prevista)
    (slot aviso-previo)
    (slot localizacao-partes)
    (slot observacoes-finais)
    (slot ajustes-futuros)
    (slot confirmacao-legislacao)
    (slot exige-garantia)
    (slot tipo-garantia)
    (slot interesse-preferencia)
    (slot meio-comunicacao)
    (slot natureza-objeto-especializada)
    (slot permite-subcontratacao)
    (slot complexidade-execucao)
    (slot riscos-externos)
    (slot duracao-contrato)
    (slot coleta-informacao)
    (slot veracidade-informacao)
    (slot condicoes-uso)
    (slot restricoes-objeto)
    (slot compromissos-danos)
    (slot riscos-danos)
    (slot peridiocidade)
    (slot transferencia-sucessao)
    (slot obrigacoes-tributarias)
    (slot natureza-juridica)
)

;Fact Flag para um fato derivado que indique se o tipo do contrato é valido.
;member$ verifica se o tipo do contrato está em uma lista de tipos válidos.
(defrule identificar-contrato-valido
    (contrato (tipo-contrato ?tipo))
    (test (member$ ?tipo (create$ aluguel cessao-direitos comodato compra-venda permuta prestacao-servicos)))
    =>
    (assert (contrato-valido))
    (assert (contrato-selecionado ?tipo))
)

;Definindo as regras para cada clausula e seus itens.

;CLAUSULA OBJETO DO CONTRATO
(defrule incluir-clausula-objeto-contrato-completo
    (contrato-valido)
    (contrato (objetivo-especifico sim))
    (contrato (partes-definidas sim))
    =>
    (assert (clausula-incluida objeto-contrato))
    (assert (clausula-itens objeto-contrato completo))
)

;CLAUSULA PRAZO
(defrule incluir-clausula-prazo-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (tempo-duracao sim))
    (contrato (peridiocidade sim))
    =>
    (assert (clausula-incluida prazo))
    (assert (clausula-itens prazo completo))
)

(defrule incluir-clausula-prazo-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (tempo-duracao sim))
    (not (contrato (peridiocidade sim)))
    =>
    (assert (clausula-incluida prazo))
    (assert (clausula-itens prazo item1 item3))
)

(defrule incluir-clausula-prazo-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (peridiocidade sim))
    (not (contrato (tempo-duracao sim)))
    =>
    (assert (clausula-incluida prazo))
    (assert (clausula-itens prazo item2 item4))
)

;CLAUSULA VALOR E FORMA DE PAGAMENTO
(defrule incluir-clausula-valor-forma-pagamento-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (existe-pagamento sim))
    =>
    (assert (clausula-incluida valor-forma-pagamento))
    (assert (clausula-itens valor-forma-pagamento completo))
)

;CLAUSULA RECISAO CONTRATUAL
(defrule incluir-clausula-recisao-contratual-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (penalidade-prevista sim))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida recisao-contratual))
    (assert (clausula-itens recisao-contratual completo))
)

(defrule incluir-clausula-recisao-contratual-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (penalidade-prevista sim))
    (not (contrato (aviso-previo sim)))
    =>
    (assert (clausula-incluida recisao-contratual))
    (assert (clausula-itens recisao-contratual item3 item4))
)

(defrule incluir-clausula-recisao-contratual-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (penalidade-prevista sim)))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida recisao-contratual))
    (assert (clausula-itens recisao-contratual item1 item2 item5))
)

;CLAUSULA FORO 
(defrule incluir-clausula-foro-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (localizacao-partes sim))
    =>
    (assert (clausula-incluida foro))
    (assert (clausula-itens foro completo))
)

;CLAUSULA DISPOSICOES GERAIS
(defrule incluir-clausula-disposicoes-gerais-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (observacoes-finais sim))
    (contrato (ajustes-futuros sim))
    (contrato (confirmacao-legislacao sim))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais completo))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (observacoes-finais sim))
    (contrato (ajustes-futuros sim))
    (not (contrato (confirmacao-legislacao sim)))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item1 item2 item4 item5))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (observacoes-finais sim))
    (not (contrato (ajustes-futuros sim)))
    (contrato (confirmacao-legislacao sim))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item1 item3 item4 item5))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-3
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (observacoes-finais sim))
    (not (contrato (ajustes-futuros sim)))
    (not (contrato (confirmacao-legislacao sim)))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item1 item4 item5))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-4
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (observacoes-finais sim)))
    (contrato (ajustes-futuros sim))
    (contrato (confirmacao-legislacao sim))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item2 item3))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-5
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (observacoes-finais sim)))
    (contrato (ajustes-futuros sim))
    (not (contrato (confirmacao-legislacao sim)))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item2))
)

(defrule incluir-clausula-disposicoes-gerais-parcial-6
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (observacoes-finais sim)))
    (not (contrato (ajustes-futuros sim)))
    (contrato (confirmacao-legislacao sim))
    =>
    (assert (clausula-incluida disposicoes-gerais))
    (assert (clausula-itens disposicoes-gerais item3))
)

;CLAUSULA GARANTIAS
(defrule incluir-clausula-garantias-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (exige-garantia sim))
    (contrato (tipo-garantia sim))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias completo))
)

(defrule incluir-clausula-garantias-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (exige-garantia sim))
    (contrato (tipo-garantia sim))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item1 item4))
)

(defrule incluir-clausula-garantias-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (exige-garantia sim))
    (not (contrato (tipo-garantia sim)))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item1 item2 item3))
)

(defrule incluir-clausula-garantias-parcial-3
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (exige-garantia sim))
    (not (contrato (tipo-garantia sim)))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item1))
)

(defrule incluir-clausula-garantias-parcial-4
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (exige-garantia sim)))
    (contrato (tipo-garantia sim))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item2 item3 item4))
)

(defrule incluir-clausula-garantias-parcial-5
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (exige-garantia sim)))
    (contrato (tipo-garantia sim))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item4))
)

(defrule incluir-clausula-garantias-parcial-6
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (exige-garantia sim)))
    (not (contrato (tipo-garantia sim)))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida garantias))
    (assert (clausula-itens garantias item2 item3))
)

;CLAUSULA DIREITO DE PREFERENCIA
(defrule incluir-clausula-direito-preferencia-completo
    (contrato-valido)
    (not (contrato-selecionado permuta))
    (contrato (partes-definidas sim))

    (contrato (interesse-preferencia sim))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida direito-preferencia))
    (assert (clausula-itens direito-preferencia completo))
)

(defrule incluir-clausula-direito-preferencia-parcial-1
    (contrato-valido)
    (not (contrato-selecionado permuta))
    (contrato (partes-definidas sim))
    (contrato (interesse-preferencia sim))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida direito-preferencia))
    (assert (clausula-itens direito-preferencia item1 item2))
)

;CLAUSULA COMUNICACOES E NOTIFICACOES
(defrule incluir-clausula-comunicacoes-notificacoes-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (localizacao-partes sim))
    (contrato (aviso-previo sim))
    (contrato (meio-comunicacao sim))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes completo))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (localizacao-partes sim))
    (contrato (aviso-previo sim))
    (not (contrato (meio-comunicacao sim)))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes completo))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (localizacao-partes sim))
    (not (contrato (aviso-previo sim)))
    (contrato (meio-comunicacao sim))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes completo))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-3
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (localizacao-partes sim))
    (not (contrato (aviso-previo sim)))
    (not (contrato (meio-comunicacao sim)))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes item1))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-4
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (localizacao-partes sim)))
    (contrato (aviso-previo sim))
    (contrato (meio-comunicacao sim))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes completo))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-5
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (localizacao-partes sim)))
    (contrato (aviso-previo sim))
    (not (contrato (meio-comunicacao sim)))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes item2 item3))
)

(defrule incluir-clausula-comunicacoes-notificacoes-parcial-6
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (localizacao-partes sim)))
    (not (contrato (aviso-previo sim)))
    (contrato (meio-comunicacao sim))
    =>
    (assert (clausula-incluida comunicacoes-notificacoes))
    (assert (clausula-itens comunicacoes-notificacoes completo))
)

;CLAUSULA USO DE TERCEIROS PARA EXECUCAO DE OBRIGACOES
(defrule incluir-clausula-uso-terceiros-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (natureza-objeto-especializada sim))
    (contrato (permite-subcontratacao sim))
    (contrato (complexidade-execucao sim))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros completo))
)

(defrule incluir-clausula-uso-terceiros-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (natureza-objeto-especializada sim))
    (contrato (permite-subcontratacao sim))
    (not (contrato (complexidade-execucao sim)))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros completo))
)

(defrule incluir-clausula-uso-terceiros-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (natureza-objeto-especializada sim))
    (not (contrato (permite-subcontratacao sim)))
    (contrato (complexidade-execucao sim))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros item2 item3 item4 item5))
)

(defrule incluir-clausula-uso-terceiros-parcial-3
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (natureza-objeto-especializada sim))
    (not (contrato (permite-subcontratacao sim)))
    (not (contrato (complexidade-execucao sim)))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros item2 item3 item4 item5))
)

(defrule incluir-clausula-uso-terceiros-parcial-4
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (natureza-objeto-especializada sim)))
    (contrato (permite-subcontratacao sim))
    (contrato (complexidade-execucao sim))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros item1 item3 item5))
)

(defrule incluir-clausula-uso-terceiros-parcial-5
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (natureza-objeto-especializada sim)))
    (contrato (permite-subcontratacao sim))
    (not (contrato (complexidade-execucao sim)))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros item1))
)

(defrule incluir-clausula-uso-terceiros-parcial-6
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (natureza-objeto-especializada sim)))
    (not (contrato (permite-subcontratacao sim)))
    (contrato (complexidade-execucao sim))
    =>
    (assert (clausula-incluida uso-terceiros))
    (assert (clausula-itens uso-terceiros item3 item5))
)

;CLAUSULA FORCA MAIOR E CASO FORTUITO
(defrule incluir-clausula-forca-maior-caso-fortuito-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (riscos-externos sim))
    (contrato (duracao-contrato sim))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito completo))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (riscos-externos sim))
    (contrato (duracao-contrato sim))
    (not (contrato (aviso-previo sim)))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito completo))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (riscos-externos sim))
    (not (contrato (duracao-contrato sim)))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito completo))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-3
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (riscos-externos sim))
    (not (contrato (duracao-contrato sim)))
    (not (contrato (aviso-previo sim)))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito completo))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-4
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (riscos-externos sim)))
    (contrato (duracao-contrato sim))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito item3 item4))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-5
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (riscos-externos sim)))
    (contrato (duracao-contrato sim))
    (not (contrato (aviso-previo sim)))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito item3 item4))
)

(defrule incluir-clausula-forca-maior-caso-fortuito-parcial-6
    (contrato-valido)
    (contrato (partes-definidas sim))
    (not (contrato (riscos-externos sim)))
    (not (contrato (duracao-contrato sim)))
    (contrato (aviso-previo sim))
    =>
    (assert (clausula-incluida forca-maior-caso-fortuito))
    (assert (clausula-itens forca-maior-caso-fortuito item3 item4))
)

;CLAUSULA CONFIRMACAO DE VERACIDADE DAS INFORMACOES
(defrule incluir-clausula-veracidade-informacoes-completo
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (contrato (aviso-previo sim))
    (contrato (confirmacao-legislacao sim))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes completo))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-1
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (contrato (aviso-previo sim))
    (contrato (confirmacao-legislacao sim))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes item1 item3 item4))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-2
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (contrato (aviso-previo sim))
    (not (contrato (confirmacao-legislacao sim)))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes item2 item3 item4))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-3
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (contrato (aviso-previo sim))
    (not (contrato (confirmacao-legislacao sim)))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes item3 item4))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-4
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (not (contrato (aviso-previo sim)))
    (contrato (confirmacao-legislacao sim))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes completo))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-5
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (not (contrato (aviso-previo sim)))
    (contrato (confirmacao-legislacao sim))
    (not (contrato (penalidade-prevista sim)))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes item1 item4))
)

(defrule incluir-clausula-veracidade-informacoes-parcial-6
    (contrato-valido)
    (contrato (coleta-informacao sim))
    (contrato (veracidade-informacao sim))
    (not (contrato (aviso-previo sim)))
    (not (contrato (confirmacao-legislacao sim)))
    (contrato (penalidade-prevista sim))
    =>
    (assert (clausula-incluida veracidade-informacoes))
    (assert (clausula-itens veracidade-informacoes item2 item3))
)

;CLAUSULA CONDICOES DE USO DO IMOVEL
(defrule incluir-clausula-condicoes-uso-imovel-completo
    (contrato-valido)
    (contrato (condicoes-uso sim))
    (contrato (restricoes-objeto sim))
    =>
    (assert (clausula-incluida condicoes-uso-imovel))
    (assert (clausula-itens condicoes-uso-imovel completo))
)

(defrule incluir-clausula-condicoes-uso-imovel-parcial-1
    (contrato-valido)
    (not (contrato (condicoes-uso sim)))
    (contrato (restricoes-objeto sim))
    =>
    (assert (clausula-incluida condicoes-uso-imovel))
    (assert (clausula-itens condicoes-uso-imovel item3 item4))
)

(defrule incluir-clausula-condicoes-uso-imovel-parcial-2
    (contrato-valido)
    (contrato (condicoes-uso sim))
    (not (contrato (restricoes-objeto sim)))
    =>
    (assert (clausula-incluida condicoes-uso-imovel))
    (assert (clausula-itens condicoes-uso-imovel item1 item2))
)

;CLAUSULA RESPONSABILIDADE POR DANOS
(defrule incluir-clausula-responsabilidade-danos-completo
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (contrato (compromissos-danos sim))
    (contrato (riscos-danos sim))
    (contrato (riscos-externos sim))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos completo))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-1
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (contrato (compromissos-danos sim))
    (contrato (riscos-danos sim))
    (not (contrato (riscos-externos sim)))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item1 item2 item4))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-2
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (contrato (compromissos-danos sim))
    (not (contrato (riscos-danos sim)))
    (contrato (riscos-externos sim))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item1 item3 item4))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-3
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (contrato (compromissos-danos sim))
    (not (contrato (riscos-danos sim)))
    (not (contrato (riscos-externos sim)))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item1 item4))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-4
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (not (contrato (compromissos-danos sim)))
    (contrato (riscos-danos sim))
    (contrato (riscos-externos sim))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item2 item3))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-5
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (not (contrato (compromissos-danos sim)))
    (contrato (riscos-danos sim))
    (not (contrato (riscos-externos sim)))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item2))
)

(defrule incluir-clausula-responsabilidade-danos-parcial-6
    (contrato-valido)
    (contrato (penalidade-prevista sim))
    (not (contrato (compromissos-danos sim)))
    (not (contrato (riscos-danos sim)))
    (contrato (riscos-externos sim))
    =>
    (assert (clausula-incluida responsabilidade-danos))
    (assert (clausula-itens responsabilidade-danos item3))
)

;CLAUSULA CONDICOES PARA RENOVACAO CONTRATUAL
(defrule incluir-clausula-renovacao-contratual-completo
    (contrato-valido)
    (contrato (peridiocidade sim))
    (contrato (aviso-previo sim))
    (contrato (ajustes-futuros sim))
    (contrato (duracao-contrato sim))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual completo))
)

(defrule incluir-clausula-renovacao-contratual-parcial-1
    (contrato-valido)
    (contrato (peridiocidade sim))
    (contrato (aviso-previo sim))
    (contrato (ajustes-futuros sim))
    (not (contrato (duracao-contrato sim)))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item1 item2 item4))
)

(defrule incluir-clausula-renovacao-contratual-parcial-2
    (contrato-valido)
    (contrato (peridiocidade sim))
    (contrato (aviso-previo sim))
    (not (contrato (ajustes-futuros sim)))
    (contrato (duracao-contrato sim))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item1 item3))
)

(defrule incluir-clausula-renovacao-contratual-parcial-3
    (contrato-valido)
    (contrato (peridiocidade sim))
    (contrato (aviso-previo sim))
    (not (contrato (ajustes-futuros sim)))
    (not (contrato (duracao-contrato sim)))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item1))
)

(defrule incluir-clausula-renovacao-contratual-parcial-4
    (contrato-valido)
    (contrato (peridiocidade sim))
    (not (contrato (aviso-previo sim)))
    (contrato (ajustes-futuros sim))
    (contrato (duracao-contrato sim))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item2 item3 item4))
)

(defrule incluir-clausula-renovacao-contratual-parcial-5
    (contrato-valido)
    (contrato (peridiocidade sim))
    (not (contrato (aviso-previo sim)))
    (contrato (ajustes-futuros sim))
    (not (contrato (duracao-contrato sim)))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item2 item4))
)

(defrule incluir-clausula-renovacao-contratual-parcial-6
    (contrato-valido)
    (contrato (peridiocidade sim))
    (not (contrato (aviso-previo sim)))
    (not (contrato (ajustes-futuros sim)))
    (contrato (duracao-contrato sim))
    =>
    (assert (clausula-incluida renovacao-contratual))
    (assert (clausula-itens renovacao-contratual item3))
)

;CLAUSULA SUCESSAO E TRANSFERENCIA DE DIREITOS
(defrule incluir-clausula-sucessao-transferencia-direitos-completo
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (transferencia-sucessao sim))
    (contrato (observacoes-finais sim))
    (contrato (aviso-previo sim))
    (contrato (ajustes-futuros sim))
    (contrato (interesse-preferencia sim))
    (contrato (riscos-externos sim))
    (contrato (confirmacao-legislacao sim))
    => 
    (assert (clausula-incluida sucessao-transferencia-direitos))
    (assert (clausula-itens sucessao-transferencia-direitos completo))
)

(defrule incluir-clausula-sucessao-transferencia-direitos-parcial-1
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (transferencia-sucessao sim))
    (contrato (observacoes-finais sim))
    (contrato (aviso-previo sim))
    (contrato (ajustes-futuros sim))
    (contrato (interesse-preferencia sim))
    (not (contrato (riscos-externos sim)))
    (not (contrato (confirmacao-legislacao sim)))
    => 
    (assert (clausula-incluida sucessao-transferencia-direitos))
    (assert (clausula-itens sucessao-transferencia-direitos item1 item3))
)

(defrule incluir-clausula-sucessao-transferencia-direitos-parcial-2
    (contrato-valido)
    (contrato (partes-definidas sim))
    (contrato (transferencia-sucessao sim))
    (not (contrato (aviso-previo sim)))
    (not (contrato (ajustes-futuros sim)))
    (not (contrato (interesse-preferencia sim)))
    (contrato (observacoes-finais sim))
    (contrato (riscos-externos sim))
    (contrato (confirmacao-legislacao sim))
    => 
    (assert (clausula-incluida sucessao-transferencia-direitos))
    (assert (clausula-itens sucessao-transferencia-direitos item2))
)

;CLAUSULA OBRIGACOES TRIBUTARIAS E FISCAIS
(defrule incluir-clausula-tributos-fiscais-completo
    (contrato-valido)
    (contrato (obrigacoes-tributarias sim))
    (contrato (natureza-juridica sim))

    (contrato (confirmacao-legislacao sim))
    
    (contrato (existe-pagamento sim))
    (contrato (penalidade-prevista sim))

    (contrato (tipo-garantia sim))
    (contrato (exige-garantia sim))
    => 
    (assert (clausula-incluida tributos-fiscais))
    (assert (clausula-itens tributos-fiscais completo))
)

(defrule incluir-clausula-tributos-fiscais-parcial-1
    (contrato-valido)
    (contrato (obrigacoes-tributarias sim))
    (contrato (natureza-juridica sim))

    (contrato (confirmacao-legislacao sim))
    
    (contrato (existe-pagamento sim))
    (contrato (penalidade-prevista sim))

    (not (contrato (tipo-garantia sim)))
    (not (contrato (exige-garantia sim)))
    => 
    (assert (clausula-incluida tributos-fiscais))
    (assert (clausula-itens tributos-fiscais item1 item4 item5))
)

(defrule incluir-clausula-tributos-fiscais-parcial-2
    (contrato-valido)
    (contrato (obrigacoes-tributarias sim))
    (contrato (natureza-juridica sim))

    (contrato (confirmacao-legislacao sim))
    
    (not (contrato (existe-pagamento sim)))
    (not (contrato (penalidade-prevista sim)))

    (contrato (tipo-garantia sim))
    (contrato (exige-garantia sim))
    => 
    (assert (clausula-incluida tributos-fiscais))
    (assert (clausula-itens tributos-fiscais item2 item3))
)