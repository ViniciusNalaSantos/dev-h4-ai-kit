---
name: cart-whatsapp
description: Implementar ou adaptar um carrinho persistente no navegador com finalização de pedido pelo WhatsApp, integrando-o à arquitetura, ao catálogo e à identidade visual de um site existente. Use quando o pedido envolver adicionar produtos, controlar variantes e quantidades, criar a página do carrinho, persistir em localStorage ou enviar o resumo pelo WhatsApp; não use para checkout com pagamento, estoque transacional ou carrinho autenticado no servidor.
---

# Carrinho com pedido pelo WhatsApp

Crie no site de destino o mesmo mecanismo funcional observado no projeto de referência, sem copiar sua aparência, seus textos, seus produtos ou sua estrutura de arquivos literalmente. O resultado deve parecer uma funcionalidade nativa do site em que está sendo implementado.

## Comece pelo site de destino

Antes de editar, inspecione:

- framework, roteamento, convenções de componentes, estado e estilização;
- modelo real de produto, identificador estável, imagens, preço quando houver e variantes como acabamento, cor ou tamanho;
- páginas/listagens onde o produto aparece e os padrões de botão já existentes;
- cabeçalho, navegação, breakpoints, tokens de cor, tipografia, espaçamento, ícones, estados vazios, modais e padrões de acessibilidade;
- configuração existente para telefone do WhatsApp, dados do cliente e variáveis de ambiente;
- implementação anterior de carrinho ou persistência, para reutilizá-la ou migrá-la sem manter duas fontes de verdade.

Não introduza React, Next.js, Tailwind ou uma biblioteca de estado apenas porque o projeto de referência os usa. Adapte a solução à pilha e às convenções já presentes. Se o site não possuir sistema visual explícito, derive padrões das telas e componentes existentes.

## Service e hook obrigatórios

Separe obrigatoriamente o mecanismo em uma **service de carrinho** e um **hook de carrinho**, como ocorre no projeto de referência. Os nomes e caminhos podem seguir as convenções do site de destino — por exemplo, `services/cart-service.ts` e `hooks/useCart.ts` —, mas as responsabilidades não devem ser misturadas nem duplicadas nos componentes.

A service deve ser a camada independente de interface responsável por:

- declarar ou importar o tipo da linha do carrinho;
- definir a chave exclusiva do `localStorage`;
- validar, ler e salvar o formato persistido;
- decidir se duas linhas representam a mesma combinação de produto e variantes;
- implementar `getCart`, `saveCart`, `addItem`, `increaseQuantity`, `decreaseQuantity`, `setQuantity` e `removeItem`, ou equivalentes coerentes com a linguagem;
- concentrar regras como incremento de item existente, remoção ao reduzir de 1 e normalização de quantidade.

A service não deve conter JSX, controlar modal, conhecer estilos nem depender de um componente específico. Sempre que possível, mantenha suas regras testáveis separadamente. Componentes de produto e da página do carrinho não devem acessar o `localStorage` diretamente; devem consumir o hook.

O hook deve ser a camada reativa responsável por:

- manter `cartItems` no estado da interface;
- carregar o valor inicial no cliente usando a service;
- expor métodos que chamam a service e atualizam o estado após cada mutação;
- expor `getItemQuantity`, `itemsCount`, `totalQuantity` e outros valores derivados realmente usados pelo site;
- assinar e limpar o evento `storage` para sincronização entre abas;
- sincronizar consumidores na mesma aba por store compartilhada ou por um evento interno, como `cartUpdated`;
- respeitar SSR/hidratação e remover listeners ao desmontar.

Use os tipos reais do catálogo e das variantes do site de destino nas assinaturas. A interface conceitual pode seguir este formato, sem exigir os mesmos nomes:

```ts
const {
  cartItems,
  itemsCount,
  totalQuantity,
  addItem,
  increaseQuantity,
  decreaseQuantity,
  setQuantity,
  removeItem,
  getItemQuantity,
} = useCart();
```

Se o projeto não for React, crie a service com as mesmas responsabilidades e a abstração reativa idiomática equivalente ao hook — por exemplo, um composable — mantendo a separação entre persistência/regras e interface. Se os dados do cliente também forem persistidos, aplique o mesmo padrão com uma service e um hook/composable próprios, sem misturá-los ao carrinho.

## Invariantes funcionais

Implemente uma única fonte de verdade para estas operações:

- ler e validar o carrinho persistido;
- adicionar um produto com a variante selecionada;
- aumentar, diminuir e definir quantidade;
- remover uma linha;
- calcular número de linhas e quantidade total;
- notificar todas as superfícies que exibem o carrinho.

Considere uma linha igual a outra pela chave composta do identificador estável do produto e de todas as variantes que distinguem a compra. No projeto de referência, a identidade é `productCode + finish`; no site de destino pode ser, por exemplo, `sku + color + size`. Adicionar a mesma combinação incrementa a quantidade. Adicionar outra combinação cria uma nova linha. Quantidade deve ser um inteiro positivo; ao diminuir de 1, remova a linha. Não use índice de array, nome visível ou posição na listagem como identidade.

Diferencie claramente:

- `itemsCount`: quantidade de linhas distintas, adequada ao indicador do carrinho quando esse for o padrão escolhido;
- `totalQuantity`: soma das unidades, adequada ao resumo do pedido.

Escolha conscientemente qual métrica o site deve mostrar no badge e mantenha rótulos acessíveis coerentes com ela.

## Modelo e localStorage

Defina tipos equivalentes aos dados reais do outro site. Use esta forma conceitual, adaptando campos e nomes:

```ts
type CartItem = {
  product: ProductSnapshot;
  variant: Record<string, string>;
  quantity: number;
};

type ProductSnapshot = {
  id: string;
  name: string;
  code?: string;
  image?: string;
  price?: number;
};
```

Armazene no `localStorage` um array JSON de linhas. O snapshot deve conter somente os dados necessários para renderizar o carrinho e montar o pedido, derivados do modelo de produto do site; não copie o tipo `Product` da referência. Se o catálogo local for a fonte autoritativa e puder ser resolvido por ID, prefira persistir IDs e seleções e reidratar os detalhes atuais. Se isso não for possível, persista um snapshot mínimo. Documente essa decisão no código.

Use uma chave exclusiva e relacionada ao site, como `<site>-cart`, nunca `samer-cart`. Se houver chance de evolução do formato, use um envelope versionado, por exemplo `{ version: 1, items: [...] }`, e trate formatos antigos explicitamente.

A camada de persistência deve:

- não acessar `window` durante SSR ou renderização no servidor;
- envolver leitura e `JSON.parse` em tratamento de erro;
- validar o formato lido: array, produto/ID válido, variantes como strings e quantidade inteira maior que zero;
- ignorar ou sanear entradas inválidas em vez de quebrar a página;
- serializar somente dados JSON seguros;
- lidar com indisponibilidade ou quota do armazenamento sem derrubar a interface;
- nunca guardar segredos, tokens ou dados de pagamento;
- evitar confiar em preço ou informação sensível vinda do navegador como valor definitivo de venda.

Após cada mutação, persista e atualize a interface imediatamente. Em aplicações com vários consumidores, ofereça um hook/store/context compartilhado. Sincronize outras abas com o evento nativo `storage`. Se a arquitetura mantiver instâncias locais do estado na mesma aba, emita também um evento interno ou use uma store que notifique seus assinantes; o evento `storage` sozinho não dispara na aba que fez a alteração. Evite piscar um carrinho vazio durante a hidratação: carregue no cliente e, quando necessário, represente explicitamente o estado “ainda não hidratado”.

Dados de identificação do cliente podem usar outra chave exclusiva, separada do carrinho, somente se forem necessários ao pedido e se o site puder justificadamente recordá-los. Colete o mínimo, permita apagar, valide antes do envio e não trate `localStorage` como armazenamento seguro.

## Botão no produto

Inclua “Adicionar ao carrinho” no componente ou página em que o usuário toma a decisão de produto. O controle deve:

- exigir todas as variantes obrigatórias antes de adicionar e explicar o que falta;
- usar a combinação selecionada para localizar a linha correta;
- ao adicionar uma combinação nova, criar quantidade 1; ao repetir, incrementar;
- mostrar feedback imediato. Quando combinar com a experiência existente, substitua o botão por controles de menos, quantidade editável e mais;
- aceitar apenas inteiros positivos no campo de quantidade e restaurar um valor válido ao perder foco;
- preservar imagem, nome, código, preço e variantes correspondentes à seleção atual;
- ser teclado-acessível, possuir rótulos claros e não depender apenas de cor para comunicar estado;
- manter áreas de toque, feedback de foco, estados desabilitados e comportamento responsivo consistentes com o site.

Adicione um acesso ao carrinho em um local coerente com a navegação existente, acompanhado do contador escolhido. Não force a posição ou o desenho usados no projeto de referência.

## Página do carrinho

Crie uma rota adequada às convenções do projeto. A página deve conter:

- título e meio previsível de voltar ou continuar comprando;
- lista das linhas com imagem, nome, código quando útil, variantes e preço quando o site trabalhar com preço;
- controles para aumentar, diminuir, digitar a quantidade e remover a linha inteira;
- estado vazio com chamada para retornar aos produtos;
- resumo com quantidade total e, quando aplicável, subtotal e observações de que o valor será confirmado;
- botão de finalização desabilitado quando o carrinho estiver vazio;
- layout responsivo e estados de foco, leitura por leitor de tela e textos alternativos adequados.

Se um item persistido não existir mais no catálogo ou uma variante tiver sido removida, informe o usuário e impeça o envio daquela linha, ou remova-a de forma transparente conforme a regra comercial do site. Não envie silenciosamente uma seleção inválida.

## Finalização pelo WhatsApp

Na página do carrinho, ofereça uma ação inequívoca como “Enviar pedido no WhatsApp”. Ela pode abrir diretamente o WhatsApp ou primeiro exibir formulário/modal de identificação, conforme as necessidades do site.

Configure o telefone fora do componente quando a infraestrutura permitir, preferencialmente por variável de ambiente pública apropriada. Normalize-o no formato internacional com apenas dígitos, sem `+`, espaços, parênteses ou hífens. Não reutilize o número do projeto de referência.

Monte uma mensagem legível contendo apenas os campos aplicáveis:

- saudação e intenção do contato;
- dados do cliente realmente necessários;
- para cada linha: código/ID, nome, variantes, quantidade e preço quando houver;
- total de unidades e valores calculados, se aplicáveis;
- observação comercial relevante, quando o pedido ainda depender de confirmação.

Gere o link no formato:

```ts
const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
```

Use quebras de linha antes de aplicar `encodeURIComponent`. Abra por ação direta do usuário, com proteção `noopener,noreferrer` quando uma nova aba for usada. Valide o formulário antes de abrir. Não coloque HTML, segredos ou dados desnecessários na mensagem. Não limpe o carrinho automaticamente após apenas abrir o WhatsApp, pois isso não confirma que a mensagem foi enviada; limpe somente quando houver uma regra explícita e um sinal confiável.

Se houver modal, siga o padrão visual e de interação do site: título associado, semântica de diálogo, fechamento por botão e `Escape`, tratamento de clique externo conforme o padrão local, foco visível, foco inicial/restauração e bloqueio de rolagem com limpeza ao desmontar.

## Identidade visual e adaptação

Reutilize componentes, tokens, ícones, tipografia e padrões responsivos existentes. Compare o resultado com as páginas adjacentes do site. A estrutura funcional da referência é transferível; estes elementos não são:

- cores cinza, preto e amarelo da Samer;
- formas de pílula e proporções específicas dos cards;
- nomes “acabamento”, `productCode` e `reference`;
- textos, telefone, chave de armazenamento, rota e dados pessoais pedidos;
- Tailwind, App Router, portais ou a separação exata de arquivos.

Prefira adaptar componentes existentes a criar uma segunda linguagem visual. Não redesenhe partes não relacionadas ao carrinho.

## Verificação

Antes de concluir, valide no mínimo:

1. adicionar produto sem variante e com cada combinação de variantes;
2. repetir a mesma combinação e adicionar combinações distintas;
3. aumentar, diminuir, digitar quantidade inválida/válida e remover;
4. recarregar a página e recuperar o carrinho;
5. abrir outra aba e observar a sincronização, quando suportada;
6. lidar com JSON corrompido e itens antigos/inválidos no `localStorage`;
7. exibir corretamente badge, estado vazio, resumo e total;
8. gerar a URL do WhatsApp com telefone, acentos, quebras de linha e todos os itens codificados;
9. impedir finalização vazia ou com variante obrigatória ausente;
10. navegar por teclado e testar larguras móvel e desktop;
11. executar os checks disponíveis no projeto, como tipos, lint, testes e build.

Ao entregar, resuma onde o mecanismo foi integrado, qual esquema/chave de persistência foi adotado, qual é a identidade de uma linha, onde o número do WhatsApp é configurado e quais verificações foram executadas.
