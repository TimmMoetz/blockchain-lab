## Dokumentation Blockchain Projekt

In dieser Dokumentation werden die wichtigsten Punkte, wie Konzept oder verwendete Technologien erläutert.

### 1. Konzept

#### 1.1 Speicherung der Blöcke

- Jeder Node speichert unabhängig die gesamte Blockchain mit den bereits validierten\
  -> Shared Nothing (Eigener CPU, RAM und Festplatte)
- Ein Block wird durch eine JSON-Datei abgebildet und gespeichert
- Der Dateiname besteht aus dem Hash des Blocks. Im Dateikörper werden die Nummer, die Zeit der Erstellung,\
  Transaktionsdaten des Blocks, sowie der Hash des vorhergehenden Blocks festgehalten



------------------------------------------------------

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/TimmMoetz/blockchain-lab/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
