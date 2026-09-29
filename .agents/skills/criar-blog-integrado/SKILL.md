---
name: criar-blog-integrado
description: Criar ou ampliar um blog em sites Next.js, reproduzindo a estrutura editorial deste projeto sem copiar sua marca. Use quando for necessário adicionar o link Blog ao header, criar a vitrine em app/blog e publicar vários artigos como componentes de página independentes em subpastas próprias, sempre adaptados ao conteúdo, à identidade visual e às convenções do site-alvo.
---

# Criar um blog integrado ao site

Implemente um blog que pareça parte original do projeto-alvo. Use a arquitetura deste projeto como referência estrutural, mas nunca replique automaticamente textos, segmento, nome, cores, imagens, contatos ou argumentos comerciais da Cedro Madeiras.

## Antes de editar

Inspecione o projeto-alvo e identifique:

- framework, roteamento, linguagem, aliases, dependências e scripts disponíveis;
- `app/page.tsx`, `app/layout.tsx`, estilos globais e configuração de tema;
- header, menu mobile, footer e componentes visuais reutilizáveis;
- tipografia, paleta, fundos, bordas, sombras, raios, espaçamentos, ícones, animações e comportamento responsivo;
- produtos, serviços, público, região atendida, diferenciais, tom de voz, logo, canais de contato e CTA principal;
- padrões já adotados para SEO, imagens, analytics, sitemap e acessibilidade.

Trate o próprio site como fonte de verdade. Não invente telefone, WhatsApp, endereço, estatísticas, certificações, depoimentos, preços ou benefícios não sustentados pelo conteúdo existente. Se um dado não estiver disponível, omita-o ou use uma chamada neutra que aponte para um canal real do projeto.

Antes de criar componentes novos, procure equivalentes já existentes. Preserve a stack e as convenções locais; não instale biblioteca apenas para reproduzir algo que o projeto já consegue fazer.

## Estrutura obrigatória

Em projetos com Next.js App Router, preserve este formato:

```text
app/
└── blog/
    ├── page.tsx
    ├── primeiro-slug/
    │   └── page.tsx
    ├── segundo-slug/
    │   └── page.tsx
    └── outros-slugs-relevantes/
        └── page.tsx
```

Crie uma pasta explícita, com `page.tsx`, para cada artigo. Use slugs curtos, descritivos, em minúsculas, sem acentos e separados por hífens. Não substitua essas várias pastas por uma única rota dinâmica, salvo quando o usuário ou a arquitetura já existente do projeto exigir conteúdo dinâmico.

### Um componente de página por artigo

Cada `app/blog/<slug>/page.tsx` deve ser um componente de página independente e conter diretamente a composição e o conteúdo editorial daquele artigo. O resultado deve ter vários componentes de página dentro de `app/blog` — um em cada pasta de slug — e não um único componente reutilizável usado para renderizar todos os slugs.

Não crie um componente genérico como `BlogPost`, `ArticlePage`, `PostTemplate` ou equivalente que receba por props ou por um objeto o título, os parágrafos, as seções, a imagem e o CTA de cada artigo. Também não reduza cada `page.tsx` a uma chamada como `<BlogPost post={...} />`, nem concentre o corpo completo dos artigos em um catálogo compartilhado para injetá-lo nos slugs. Mesmo quando duas páginas têm estrutura visual parecida, escreva em cada `page.tsx` seu próprio componente, metadata, cabeçalho, corpo, seções e CTA, seguindo o padrão de páginas independentes deste projeto de referência.

É permitido compartilhar apenas elementos pequenos e verdadeiramente transversais da interface, como botão de voltar, breadcrumb, ícone, formatação de data ou card da vitrine. Esses elementos não podem encapsular a página inteira nem receber o conteúdo completo do artigo. Um catálogo comum pode alimentar os cards de `app/blog/page.tsx` e armazenar campos curtos usados para manter a listagem sincronizada, mas o texto editorial e a composição de cada post devem permanecer no `page.tsx` do respectivo slug.

## Integrar o header

Adicione a opção **Blog** ao header existente, apontando para `/blog`.

- Inclua o item tanto na navegação desktop quanto no menu mobile.
- Preserve ordem, estilo, estados de hover/foco, animações e comportamento de fechamento do menu.
- Use o componente de link já adotado pelo projeto para rotas internas.
- Não trate `/blog` como seletor de rolagem. Se o header mistura rotas e âncoras, diferencie os dois comportamentos.
- Garanta que links para seções da home funcionem também fora da página inicial; quando necessário, use caminhos como `/#contato` em vez de apenas `#contato`.
- Se o projeto mantém header e footer globais, conserve-os no blog. Se eles são montados por página, siga a convenção existente e evite duplicações acidentais.

## Criar a vitrine em `app/blog/page.tsx`

A página principal deve seguir a mesma linguagem visual do restante do site e oferecer, no mínimo:

- título e introdução coerentes com a marca e o nicho;
- uma lista central de artigos com `slug`, título, resumo, data, tempo de leitura, categoria e, se o layout usar, imagem, ícone e estado de destaque;
- um artigo em destaque quando isso fizer sentido para a composição visual;
- grade responsiva de cards que leve a `/blog/<slug>`;
- data legível, categoria, resumo e indicação clara para abrir o artigo;
- busca por título, resumo ou categoria e filtro por categoria, como no projeto de referência;
- estado vazio quando nenhum artigo corresponder aos filtros;
- navegação por teclado, foco visível, contraste adequado e controles com rótulos acessíveis.

Faça a busca e os filtros no cliente somente quando houver interatividade real. Mantenha o máximo possível como Server Component e isole a parte interativa em um Client Component se isso preservar metadata e reduzir JavaScript. Não force essa separação se contrariar a organização simples já usada pelo projeto.

Derive categorias dos artigos para evitar divergência. Ordene os posts do mais recente para o mais antigo e mantenha somente um destaque principal, salvo outra regra explícita do projeto.

## Criar os artigos

Crie vários artigos iniciais — normalmente entre 6 e 10 quando o usuário não indicar quantidade — cobrindo assuntos realmente relacionados ao site. Distribua os temas entre intenção informacional, dúvidas frequentes, comparação, escolha, uso, manutenção, tendências ou contexto local apenas quando essas frentes fizerem sentido para o negócio.

### Imagens editoriais externas

Pesquise imagens próprias para cada artigo no Unsplash ou em outra fonte online confiável. Não reutilize imagens, fotografias ou banners que já existam no projeto-alvo para cards, capas ou conteúdo dos artigos, mesmo que pareçam relacionados ao tema. Essa restrição não impede o uso dos elementos de identidade necessários à interface, como logo e ícones do próprio site.

- escolha imagens diretamente relacionadas ao assunto de cada artigo e coerentes entre si, sem repetir a mesma imagem em posts diferentes;
- prefira fontes que permitam o uso pretendido e respeite licença, crédito e atribuição quando exigidos; não copie imagens de resultados de busca sem confirmar sua origem e condições de uso;
- verifique se a URL e a imagem realmente abrem, use uma URL estável e evite endpoints aleatórios que possam trocar o conteúdo depois da publicação;
- selecione resolução e proporção adequadas para capa, card e compartilhamento social, evitando arquivos desnecessariamente pesados;
- configure o domínio remoto em `next.config` quando `next/image` exigir e preserve as regras de segurança já adotadas pelo projeto;
- escreva `alt` descritivo conforme o conteúdo visual e o contexto do artigo, sem repetir o título apenas para inserir palavras-chave;
- mantenha, no catálogo compartilhado dos posts, a URL, o texto alternativo e, quando necessário, a origem ou o crédito da imagem para que card, artigo e metadata usem os mesmos dados.

Se uma imagem adequada e licenciada não puder ser confirmada, procure outra fonte online em vez de recorrer às imagens existentes do projeto ou deixar uma URL não verificada.

Cada `app/blog/<slug>/page.tsx` deve conter:

- metadata própria com título e descrição específicos; inclua canonical, Open Graph ou keywords somente conforme o padrão do projeto;
- link claro para voltar a `/blog`;
- categoria, data e tempo estimado de leitura;
- um único `h1`, introdução e seções semânticas organizadas com `h2` e, quando necessário, `h3`;
- conteúdo útil, original e coerente com o nível de conhecimento do público;
- links internos relevantes, sem repetição artificial de palavras-chave;
- CTA final baseado em um canal ou ação real do site;
- a imagem editorial externa selecionada para o artigo quando ela acrescentar valor, tecnicamente configurada e com `alt` adequado.

Adapte o estilo do artigo à identidade encontrada: largura de leitura, fundo, cores, tipografia, bordas, blocos de destaque, ícones, animações e espaçamento devem conversar com a home. Reutilize as classes e os componentes existentes. Não imponha o fundo escuro, o verde, o WhatsApp ou o vocabulário da Cedro a outro site.

Não transforme artigos em páginas de venda vazias. Responda de fato à intenção do título, use linguagem natural, evite texto genérico e não faça alegações factuais que o site não sustenta. Datas não podem ficar no futuro por engano. Calcule um tempo de leitura plausível a partir do texto, em vez de usar o mesmo valor em todos os posts.

## Manter tudo sincronizado

Para cada artigo publicado, confirme que:

1. existe uma pasta `app/blog/<slug>/page.tsx`;
2. o mesmo slug aparece na listagem da vitrine;
3. título, descrição, categoria, data e tempo de leitura coincidem entre card, metadata e página;
4. o card abre uma rota válida;
5. a rota `/blog` e todos os artigos entram no sitemap quando o projeto mantém um sitemap manual;
6. qualquer catálogo compartilhado, dado estruturado ou feed já existente também foi atualizado.

Inclua `/blog` no sitemap, não apenas os artigos. Use a URL base real já configurada no projeto e não introduza um segundo domínio divergente. Se o sitemap for gerado a partir dos arquivos ou de uma fonte central, integre-se a esse mecanismo em vez de manter uma lista paralela.

## SEO e qualidade técnica

- Preserve o idioma e a codificação UTF-8 do projeto.
- Use HTML semântico e hierarquia correta de headings.
- Evite títulos, descrições e slugs duplicados.
- Não use `use client` em uma página que exporta `metadata`; mova a interação para um componente cliente quando necessário.
- Quando o projeto adotar dados estruturados, gere `BlogPosting` com dados reais e consistentes, sem criar informações ausentes.
- Evite links externos decorativos. Para links externos reais, aplique as práticas de segurança já usadas pelo projeto.
- Não deixe placeholders, números fictícios, imports sem uso, links quebrados ou imagens remotas sem configuração.
- Confira o layout em larguras mobile e desktop e respeite preferências de movimento reduzido quando houver animações.

## Verificação

Ao terminar:

1. confira a árvore de `app/blog` e compare os slugs com o catálogo da vitrine e o sitemap;
2. procure placeholders e referências indevidas à Cedro Madeiras ou a outro projeto de origem;
3. confirme que as imagens dos artigos vieram do Unsplash ou de outra fonte online válida, que nenhuma imagem editorial existente do projeto foi reutilizada e que URLs, créditos e configuração de domínios remotos estão corretos;
4. execute os scripts de typecheck e lint disponíveis no `package.json`;
5. execute o build quando for viável e proporcional ao projeto;
6. corrija erros causados pela implementação sem alterar conteúdo não relacionado;
7. confirme que cada slug possui seu próprio componente de página e que nenhum componente ou template genérico renderiza o corpo completo de vários artigos.

Considere a tarefa concluída somente quando o item Blog aparece e funciona nos menus aplicáveis, a vitrine está responsiva e coerente com a marca, todas as subpastas de artigos abrem corretamente, os conteúdos pertencem ao nicho do site e as rotas relevantes estão cobertas pelo mecanismo de SEO do projeto.
