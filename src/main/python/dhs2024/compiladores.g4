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
ANDsim : '&'; 
OR : '||';
ORsim: '|'; 
POT: '^'; 
DESPizq: '<<'; 
DESPder: '>>'; 


NUMERO : DIGITO+ ;

INT:'int';
CHAR:'char';
FLOAT:'float';
BOOLEAN:'bool';
DOUBLE:'double';
VOID: 'void';
RETURN: 'return';

tipodato: INT | CHAR | FLOAT | BOOLEAN | DOUBLE ;

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

WHILE :'while';
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
            // | declAsig PYC 
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

declaracion : tipodato ID (COMA ID)*; // int x, y, z
// declAsig : declaracion ASIG opal //int x=chule+bauti
//        | declaracion ASIG callFunction
//        ; 

// declAsigNuevo : tipodato ID ASIG opal (COMA tipodato ID ASIG opal)* (COMA)

///////////////////// FUNCION
prototipoFuncion : tipodato ID PA (parFunc)? PC PYC ; //Este es el prototipo con ;

prototSpyc :
            tipodato ID PA (parFunc)? PC // int x (int y, int z) Tambien acepta int x (int y)
           | VOID ID PA PC
           | VOID ID PA parFunc PC
           ; 

parFunc : tipodato ID (COMA tipodato ID)* ; // El asterisco indica que pueden haber una o mas 'parejas' de coma declaracion
                                            // no se puede poner (COMA parFunc)* porque toma mal los datos en el escucha

funcion : prototSpyc bloque; 

callFunction : ID PA envPar PC ; // Llamada a funcion

envPar : opal lista_envPar | ; // Parametros enviados en la llamada
lista_envPar : COMA opal lista_envPar | ; // Lista de parametros separados por comas

////////////////////// FIN FUNCION
asignacion: ID ASIG opal 
          // | ID opComp ASIG opal //x+=operacion
          | ID ASIG callFunction
          //| incremento
          | decremento
          ;

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

//iwhile : WHILE PA ID PC instruccion ;//llave es instruccion compuesta, despues del while una instruccion
  iwhile : WHILE PA cond PC bloque ;

bloque : LLA instrucciones LLC; 

//for :
ifor : FOR PA init PYC cond PYC iter PC bloque //Cambie instruccion por bloque y tambien en if y else
    //  | FOR PA declAsig PYC cond PYC iter PC bloque 
     ;

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
//fin for

//if
iif : IF PA opal PC bloque ; //Modifique el nombre con una i adelante para que señale instruccion
ielse : ELSE bloque ;        //y tambien los modifique donde se los usaba