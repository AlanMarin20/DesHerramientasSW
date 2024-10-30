grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

PA: '(' ;
PC: ')' ;
LLA: '{' ; 
LLC: '}' ;
PYC: ';' ;
COMA: ',' ;
SUMA : '+' ;
RESTA : '-' ;
MULT : '*' ;
DIV : '/' ;
MOD : '%' ; 
ASIG: '=' ;
INCR : '++' ;
DECR : '--' ; 

MAYOR : '>' ;
MAYOREQ : '>=' ;
MENOREQ : '<=' ;
MENOR : '<' ;
IGUAL : '==' ;
AND : '&&' ;
ANDsim : '&' ; 
OR : '||' ;
ORsim: '|' ; 
POT: '^' ; 
DESPizq: '<<' ; 
DESPder: '>>' ; 

NUMERO : DIGITO+ ;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

//----TIPOS DE DATOS----
tipodato: INT | CHAR | FLOAT | BOOLEAN | DOUBLE ;
INT:'int' ;
CHAR:'char' ;
FLOAT:'float' ;
BOOLEAN:'bool' ;
DOUBLE:'double' ;
VOID: 'void' ;
RETURN: 'return' ;

//----OPERACIONES----
opComp: SUMA 
      | RESTA
      | MULT
      | DIV
      | MOD
      | ANDsim
      | ORsim
      | POT
      | DESPder
      | DESPizq
      ;

opal: or ; 

or : and o ;

o : OR and o 
    |
    ;

and : comp a ;

a : AND comp a 
   |
   ;

comp: exp c; //c es una comparacion prima

c : MAYOR exp c
  | MENOR exp c
  | MENOREQ exp c
  | MAYOREQ exp c
  | IGUAL exp c
  |
  ;
  
exp : term e ; //e es una expresion prima

term : factor t; //t es termino prima, es una multiplicacion y viene un factor

e : SUMA term e // a partir del segundo termino
  | RESTA term e
  | //regla vacia 
  ;
t : MULT factor t  //esto es jerarquico, las multiplicaciones e hacen antes y hacen que este por abajo del arbol
  | DIV factor t
  | MOD factor t
  |
  ;
factor : NUMERO  //parentesis es factor
      | ID
      | PA or PC
      ;

//----PROGRAMA----

programa : instrucciones EOF ; //secuencia de instrucciones hasta el final del archivo

//----INSTRUCCIONES----

instrucciones : instruccion instrucciones //Es una instruccion con mas instrucciones 
              |                           // o con nada
              ;

instruccion: declaracion PYC //Que hay dentro de una instruccion
            | declAsig PYC
            | iwhile
            | ifor
            | iif
            | ielse
            | bloque
            | asignacion PYC
            | prototipoFuncion
            | funcion
            | RETURN opal PYC 
            | callFunction PYC
            ;

declaracion : tipodato ID (COMA ID)*; // int x, y, z sin ;

declAsig : declaracion ASIG opal //int x = chule + bauti sin ;
       | declaracion ASIG callFunction // int x = funcion() sin ;
       ; 

asignacion: ID ASIG opal // x = operacion
          | ID opComp ASIG opal // x += operacion
          | ID ASIG callFunction // x = funcion() sin ;
          | incremento // i++
          | decremento // i--
          ;

//----FUNCION----

prototipoFuncion : tipodato ID PA (parFunc)* PC PYC ; //int funcion (con y sin parametros); 

prototSpyc : tipodato ID PA PC // int x ()
           | tipodato ID PA parFunc PC // int x (int y, int z) Tambien int x (int y)
           | VOID ID PA PC
           | VOID ID PA parFunc PC
           ; 

parFunc : tipodato ID (COMA tipodato ID)* ; // El asterisco indica que pueden haber una o mas 'parejas' de coma declaracion
                                            // no se puede poner (COMA parFunc)* porque toma mal los datos en el escucha

funcion : prototSpyc bloque; //Cuerpo de la funcion 

callFunction : ID PA (envPar)* PC ; // Llamada a funcion

envPar : opal lista_envPar; // Parametros enviados en la llamada
      
lista_envPar : COMA opal lista_envPar // Lista de parametros separados por comas
            | 
            ; 

//----FIN FUNCION----

bloque : LLA instrucciones LLC; // { instrucciones }

WS : [ \t\n\r] -> skip;

//----BUCLES----
//--Declaraciones de palabras reservadas de bucles--
WHILE :'while';
FOR: 'for';
IF: 'if' ;
ELSE: 'else' ;

//--Cuerpos de los bucles--
iwhile : WHILE PA cond PC bloque ; // Cuerpo de la instruccion while

ifor : FOR PA init PYC cond PYC iter PC bloque 
     | FOR PA declAsig PYC cond PYC iter PC bloque 
     ;

iif : IF PA opal PC bloque ;

ielse : ELSE bloque ; 

//Cosas necesarias para el for
init : ID ASIG NUMERO ;
cond : opal;
iter : asignacion
      | incremento
      | decremento 
      ;
incremento : ID INCR
           | INCR ID ;
decremento : ID DECR 
           | DECR ID;

