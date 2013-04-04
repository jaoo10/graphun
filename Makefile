PYTHON=python2.7 -B

.PHONY: testar testar-bfs testar-ts testar-scc testar-mst atualizar

testar:
	@echo "** Testando todos **"
	@$(PYTHON) testador/main.py "bfs|ts|scc|mst" src/ testes/

testar-bfs:
	@echo "** Testando bfs **"
	@$(PYTHON) testador/main.py bfs src/ testes/

testar-ts:
	@echo "** Testando ts **"
	@$(PYTHON) testador/main.py ts src/ testes/

testar-scc:
	@echo "** Testando scc **"
	@$(PYTHON) testador/main.py scc src/ testes/

testar-mst:
	@echo "** Testando mst **"
	@$(PYTHON) testador/main.py mst src/ testes/

atualizar:
	@git pull

zip: src.zip

src.zip: $(shell find src/ -type f ! -path 'src/*/target/*' ! -name '*~')
	@if grep -q -P '\000' $?; then\
        echo "** Arquivos binários encontrados **";\
        grep -l -P '\000' $?;\
        echo "** Remova os arquivos binários antes de fazer o envio **";\
        echo "** Se você estiver usando um IDE, procure pela opção Clean **";\
        exit 1; fi
	@echo Criando arquivo src.zip.
	@zip --quiet src.zip -r $?
	@echo Arquivo src.zip criado.

enviar: src.zip
	@$(PYTHON) enviar.py src.zip

limpar-log:
	@echo Removendo arquivos de log
	@rm *.log

limpar: limpar-log
	@echo Removendo src.zip
	@rm -f src.zip

limpar-target:
	@rm -rf $$(find src/ -path 'src/*/target')
