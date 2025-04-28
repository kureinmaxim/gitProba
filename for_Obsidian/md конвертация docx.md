#markdown #chocolatey

![[Pasted image 20250421143727.png|500]]
==Установить **Pandoc** с помощью **Chocolatey**== на Windows 11
В той же **PowerShell (от администратора)** выполни:
```powershell
choco --version
choco install pandoc -y
pandoc --version
```

==Конвертация==
Допустим, у  есть файл `example.md`
```powershell
cd "C:\путь\к\твоей\папке"

pandoc example.md -o example.docx
```
Дополнительно:
Хочешь использовать свой шаблон Word (например, со своими стилями заголовков и шрифтами)?
```powershell
pandoc example.md -o example.docx --reference-doc=шаблон.docx
```