grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

// INST : (LETRA | DIGITO | [- ,;{}()+=>])+ '\n';
PA : '(' ;
PC : ')' ;
LLA : '{' ;
LLC : '}' ;
PYC : ';' ;
SUMA : '+' ;
RESTA : '-' ;
MULT : '*' ;
DIV : '/' ;
MOD : '%' ;
MAY : '>' ;
MEN :'<';
MAYI : '>=' ;
MENI : '<=' ;
DIS : '!=' ;

ASIG : '=';
IGUAL : '==';

NUMERO : DIGITO+ ;

INT : 'int';
WHILE : 'while';
FOR : 'for';
IF : 'if';

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
WS : [ \t\n\r] -> skip;

// OTRO : . ;
// s : ID     {print("ID ->" + $ID.text + "<--") }         s
//   | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
//   | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
//   | EOF
//   ;

// si : s EOF ;

// s : PA s PC s
//   |
//   ;
programa : instrucciones EOF ;

instrucciones : instruccion instrucciones 
              |
              ;

// instruccion : INST {print($INST.text[:-1])} ;
instruccion : declaracion 
            | iwhile
            | ifor
            // | iif
            | bloque
            | asignacion PYC
            ;

declaracion : INT ID PYC ;
asignacion : ID ASIG opal ;
opal : exp log 
    | sJuntos ID
    | ID sJuntos
    ; 
log : comp // Logica
    | igDis 
    |
    ;
sJuntos : SUMA SUMA
    | RESTA RESTA
    ;
comp : MAY exp //Comparacion
    | MEN exp
    | MAYI exp
    | MENI exp
    ;
igDis : IGUAL exp //Igual o distinto
    | DIS exp
    ;
exp : term e ; //Expresion
e   : SUMA term e
    | RESTA term e 
    |
    ;
term : factor t; //Termino
t   : MULT factor t
    | DIV factor t
    | MOD factor t
    |
    ;
factor : NUMERO 
    | ID
    | PA exp PC
    ;

iwhile : WHILE PA ID PC instruccion ;//llave representa una instruccion compuesta, despues del while viene siempre una instruccion
ifor : FOR PA init PYC cond PYC iter PC instruccion;
init : asignacion
    |
    ;
cond : opal
    ;
iter : opal
    |
    ;
iif : IF PA cond PC instruccion
    | IF PA PC instruccion
    | IF PA NUMERO PC instruccion
    | IF PA ID PC instruccion
    ;
bloque : LLA instrucciones LLC; 
