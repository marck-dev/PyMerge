# PyMerge

PyMerge has two variants:
- **PyMerge OptionFile** witch process the pymerge config file and concatenate the files as specified in the file.
- **PyMerge Compiler** whitch compile the file that passed as argument and interpreted line by line of the file searching the specific command to execute.
---
## PyMerge OptionFile
Read the `pymerge` file and concatenate the files.
Example:
```
outFile "mi_concat_file_name"
import "file1.txt"
import "file2.txt"
```
- `outFile "<name>"` set the output file name
- `import "<file>"` set to concatenate file to the output file

The tool will follow the documet order.

## PyMerge Compiler
The compiler read the file that pass as argument and process it, line by line looking for keywords.

This keywords can be a long the file in a line of comment and it has a specific format:
`# !cmd <arg>`.

Example:
### File a.js
```javascript
function action(msg){
    alert(msg);
}
```
### File b
```javascript
\\ !outFile "HelloWorld.js"
\\ !import "a.js"

action("Hello World");
```

### HelloWorld.js
```javascript
function action(msg){
    alert(msg);
}

action("Hello World");
```

! Only accept one line comments and the most commons comment chars: `//` and `#`.
For insert a command in multiline comment or in other comments tags:

This hasn't got sense:
```

/*
    multiline comment
    // !import "file.js"
*/

```
This is more usefull for lenguage that only have multiline comments
```
/* # !import "file.sql" */

for HTML
<!-- # !import "header.html" -->
```

In the copiler the command are similar:
- `[// | #] !import "<file name>"` - for compile an import the file
- `[// | #] !outFile "<file_name>"` - to set the final name of the out file