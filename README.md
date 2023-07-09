# Findata web-app

_A aplicação web de dados da Secretaria de Finanças da prefeitura cidade do Recife._

#### Aqui se encontra dashboards de:

- Receita tributária (DAMs pagos)
- CAF (comissão administrativa fiscal)
- CAPAG (capacidade de pagamento dos entes federativos)
- RREE3-Anexo3 do Sincofi (relatório de execução orçamentária resumida)
- Monitoramento da SEFIN
- Central de previsões.

## Rodar a aplicação localmente

```bash
# clonando e configurando ambiente
$ git clone https://github.com/SEFIN-GGIE/findatawebapp.git
$ cd findatawebapp; python -v venv ve; source ve/bin/activate; 
$ python -m pip install -U pip; pip install requirements.txt

# rodando a app na porta 5000
$ flask run
```

Datasets ficam em findatawebapp/app/dashboards/_datasets

## Como configurar para rodar num servidor Ubuntu

Fonte: [clique aqui](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)


#### 1. Primeiros passos: trazendo o projeto pra máquina

```bash
# certificando da atualização e instalação de pacotes no sistema operacional
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# clonando e configurando ambiente
$ git clone https://github.com/SEFIN-GGIE/findatawebapp.git
$ cd findatawebapp; python -v venv ve; source ve/bin/activate; 
$ python -m pip install -U pip; pip install requirements.txt

```

#### 2. Criando um serviço para o projeto estar sempre no ar

Crie e abra um arquivo com o comando

```bash
sudo nano /etc/systemd/system/findatawebapp.service
```

e cole neste arquivo:

```bash
[Unit]
Description=Gunicorn instance to serve findata app
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/findatawebapp
Environment="PATH=/home/ubuntu/findatawebapp/ve/bin"
ExecStart=/home/ubuntu/findatawebapp/ve/bin/gunicorn --workers 2 --bind unix:findata.sock -m 007 findata:server

[Install]
WantedBy=multi-user.target
```

Importante: observe que o usuário e grupo de arquivos é 'ubuntu', para o ver quais são o da sua máquina faça
```bash
$ ll findatawebapp/
```

Para mudar o user e o group de uma pasta leia [aqui](https://linuxhint.com/change-directory-owner-linux/#:~:text=chown%20command%20syntax&text=Utilize%20the%20%E2%80%9CUser%E2%80%9D%20for%20the,want%20to%20change%20the%20ownership.)

#### 3. Iniciando o serviço

```bash
$ sudo systemctl start findatawebapp
$ sudo systemctl enable findatawebapp

# para ver o status, se está tudo ok
$ sudo systemctl status findatawebapp
```

#### 4. NGINX

Edite o arquivo

```bash
$ sudo nano /etc/nginx/sites-available/myproject/default
```

E faça as inclusões devidas:

```bash
server {
    listen 80;
    # caso tenha algum dominio, descomente e insira abaixo
    # server_name your_domain www.your_domain;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/findatawebapp/findata.sock;
    }
}
```

```bash
# link o arquivo com o da outra pasta
$ sudo ln -s /etc/nginx/sites-available/deafult /etc/nginx/sites-enabled

# verifique se tudo deu certo
$ sudo nginx -t

# caso sim, reinicie o nginx
$ sudo systemctl restart nginx
```

Se o NGINX apresentar erros, os comandos para logs para verificação do que aconteceu estão:

- sudo less /var/log/nginx/error.log (log de erros)
- sudo less /var/log/nginx/access.log (log de acessos)
- sudo journalctl -u nginx (log do serviço nginx)
- sudo journalctl -u findatawebapp (log do serviço criado pro findata)

#### 5. Abrindo a porta 80 para internet

Usando ufw:

```bash
$ sudo ufw delete allow 80
$ sudo ufw allow 'Nginx Full'
```


Às vezes, algumas máquinas só aceitam abrir uma porta com uso de iptables

```bash
$ sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
$ sudo netfilter-persistent save
```

Agora com o serviço e o nginx configurados e ativos é aplicação estará disponivel em http://seu.endereço.de.ip/findata

Caso seja uma máquina da PCR, veja com o administrador de redes se é preciso desabilitar o firewall.

Para configuração de https, use o link q foi passado como fonte desse tutorial.

## Adicionando um novo dashboard ao Findata

#### a. Coloque um novo projeto dash na pasta findatawebapp/app/dashboards

Observações:

- Não existe a inicialização de um web-server como é padrão das aplicações Dash.
- Afinal, o próprio web-server é a aplicação Flask do Findata
- Use a estrutura de arquivos dos outros dashboards. 
- Tenha um arquivo layout.py onde será a página do dashboard e será abastecida das demais páginas do projeto.
- Tenha um arquivo callbacks.py que concetrará todos os callbacks do dashboard.


#### b. Modifique o arquivo __init__.py em findatawebapp/app
 
 - Observe que da linha 51 a 75 é onde fica os registros de cada dashboard, é só repetir essa assinatura.
 - entenda como funciona a função `register_dash_app`, onde:

 ```python
 def register_dash_app(pp, title, base_pathname, layout, callback_funcs)
    app: a aplicação flask
    title: nome do dashboard que ficará no head da página
    base_pathname: o endereço da página (http://endereço-ip/dashboards/meu-dashboard/)
    layout: arquivo de layout (o layout.py do novo Dash)
    layout: arquivo de callback (o callback.py do novo Dash)
 
 ```

 Para uma melhor compreensão desse tema, clique [aqui](https://hackersandslackers.com/plotly-dash-with-flask/)

## Adicionando um novo usuário à aplicação

Na pasta do projeto:

```bash
$ flask shell
```

Abrirá uma instância do findata como linha de código.

```python
>>> u = User(username='fulano.detal', email='fulanodetal@recife.pe.gov.br')
>>> u.set_password('123456')
>>> db.session.add(u)
>>> db.session.commit()
>>> exit()
```

Para remover:
```python
>>> # digamos que queremos remover o usuário de id 1
>>> u = User.query.get(1)
>>> db.session.delete(u)
>>> db.session.commit()
>>> exit()
```

Para se ter uma melhor compreensão, clique [aqui](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)


