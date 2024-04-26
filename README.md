# Trabalho de desenvolvimento bimestral referente a matéria optativa de Processamento de Imagens e Reconhecimento de Padrões

![image](https://github.com/Dyest/Interface-PDI/assets/64050916/e11cc5f2-cd80-4482-86a2-02c1ae0a1452)

Este é um projeto desenvolvido para a matéria de Processamento de Imagens e Reconhecimento de Padrões. Desenvolvido em Python utilizando as bibliotecas Tkinter, OpenCV e Pillow. O objetivo deste projeto é oferecer uma ampla gama de recursos para o processamento e manipulação de imagens, como conversões de cor, aplicação de filtros, detecção de bordas, binarização e morfologia matemática através de uma interface simples e intuitiva. 

## Recursos 
- **Conversão de Cores:** O usuário pode converter a imagem enviada para os padrão de cor RGB -> CIE L*a*b*, RGB -> XYZ, RGB -> HSV e RGB -> Gray.
- **Aplicação de Blur:** O usuário pode Aplicar Blur Bilateral na imagem enviada.
- **Identificação de Bordas:** O usuário pode aplicar o filtro Canny, para identificar bordas através dos limiares superior e inferior.
- **Aplicação de Threshold:** O usuário pode converter a imagem enviada para Threshold Gray.
- **Aplicação de Morfologia:** O usuário pode aplicar morfologias de Dilatação na imagem enviada.
- **Histórico de Atividades e Deleção:** A aplicação possui um histórico de atividades executadas na imagem, exibindo o histórico sequencial das transformações aplicadas. Além de poder deletar qualquer um deles, independente da ordem. 
- **Preview:** A aplicação fornece em tempo real uma imagem preview, com as conversões e aplicações feitas nela alem de apresentar a imagem original para comparação.
- **Salvamento de imagem:** A aplicação fornece ao usuário a opção de salvar uma cópia da imagem modificada em seu sistema.
- **Controle de erros** A aplicação possui um sistema de controle de erros básicos, evitando complicações e informando os problemas ao usuário.


## Requisitos
Requisitos necessarios: Python 3 e as bibliotecas Tkinter, OpenCV e Pillow.


## Instalação
#### Repositório do projeto:
git clone [https://github.com/ana-cdk/pdi-bimestral1.git](https://github.com/Dyest/Interface-PDI.git)


### Dependências:
pip install -r requirements.txt


## Utilização
1. Clone o repositório do GitHub.
2. Instale as dependencias utilizadas.
3. Execute o aplicativo em uma IDE, dentro da raiz do projeto atravez do comando "python interface.py".
