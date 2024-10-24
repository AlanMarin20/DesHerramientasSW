grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

//INST : (LETRA | DIGITO | [- ,;{}()+=>] )+ '\n'; es una letra, un digito .. no quiero que exceda el guion 
PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
COMA: ',';
SUMA : '+';
RESTA : '-';
MULT : '*';
DIV : '/';
MOD : '%'; 
ASIG: '=';
INCR : '++';
DECR : '--' ; 

MAYOR : '>';
MAYOREQ : '>=';
MENOREQ : '<=';
MENOR : '<';
IGUAL : '==';
AND : '&&';
ANDsim : '&'; // agregado 24/10
OR : '||';
ORsim: '|'; // agregado 24/10
POT: '^'; // agregado 24/10
DESPizq: '<<'; // agregado 24/10
DESPder: '>>'; // agregado 24/10


WHILE :'while';
NUMERO : DIGITO+ ;

INT:'int';
CHAR:'char';
FLOAT:'float';
BOOLEAN:'bool';
DOUBLE:'double';
RETURN: 'return';

tipodato: INT | CHAR | FLOAT | BOOLEAN | DOUBLE ;

opComp: SUMA // agregado 24/10
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

FOR: 'for';
IF: 'if' ;
ELSE: 'else' ;

WS : [ \t\n\r] -> skip;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
/*OTRO : . ;


s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
  | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
  | EOF
  ;
  */

//si : s EOF; que comience en un nodo, que sea solo la razi del arbol
//s: PA s PC s  s permite la anidacion, se cierra un parentesis y se puede abrirotro parentesis. Verifica balance de parentesis
  //|
//;

programa : instrucciones EOF ; //secuencia de instrucciones hasta el final del archivo

instrucciones : instruccion instrucciones //es una instruccion con mas instrucciones 
                |
                ;

instruccion: declaracion PYC
            | declAsig PYC
            | iwhile
            | ifor
            | if
            | else
            | bloque
            | asignacion PYC
            | prototSpyc PYC 
            | funcion
            | RETURN exp PYC 
            ;

declaracion : tipodato ID ; // int x
declAsig : declaracion ASIG NUMERO // int x = 5;
       | declaracion ASIG ID // int x = a;
       | declaracion ASIG opal //int x=chule+bauti
       ; 


prototSpyc :tipodato ID PA PC // int x ()
           | tipodato ID PA parFunc PC; // int x (int y, int z) Tambien acepta int x (int y)

parFunc : tipodato ID (COMA tipodato ID)* ; // El asterisco indica que pueden haber una o mas 'parejas' de coma declaracion
                                            // no se puede poner (COMA parFunc)* porque toma mal los datos en el escucha

funcion : prototSpyc bloque; 

asignacion: ID ASIG opal 
          | ID opComp ASIG opal; //x= operacion 

opal: or;  //completar una operacion aridmeticas, buscar en cppreference, agregamoss operaciones relacionales

or : and o ;

o : OR and o 
    |
    ;

and : comp a ;

a : AND comp a 
   |
   ;

comp: exp c;

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


t :   MULT factor t  //esto es jerarquico, las multiplicaciones e hacen antes y hacen que este por abajo del arbol
    | DIV factor t
    | MOD factor t
    |
    ;
factor : NUMERO  //parentesis es factor
      | ID
      | PA or PC
      ;

iwhile : WHILE PA ID PC instruccion ;//llave es instruccion compuesta, despues del while una instruccion

bloque : LLA instrucciones LLC; 

//for :
ifor : FOR PA init PYC cond PYC iter PC instruccion;
init : ID ASIG NUMERO ;
cond : opal;
iter : asignacion
      | incremento
      | decremento 
      | preincremento
      | predecremento
      ;
incremento : ID INCR ;
decremento : ID DECR ;
preincremento : INCR ID ;
predecremento : DECR ID ;
//fin for

//if
if : IF PA opal PC instruccion ;
else : ELSE instruccion ;