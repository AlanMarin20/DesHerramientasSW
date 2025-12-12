grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

//INST : (LETRA | DIGITO | [- ,;{}()+=>] )+ '\n'; es una letra, un digito .. no quiero que exceda el guion 
PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
CA: '[';
CC: ']';
COMs: '\''; 
COMd: '"';
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
DIFERENTE : '!=';
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
            | declaracionArreglos PYC
            | declAsig PYC 
            | iwhile
            | ifor
            | iif
            | ielse
            | bloque
            | asignacion PYC
            | prototipoFuncion
            | funcion
            | ireturn PYC
            | callFunction PYC
            ;

ireturn : RETURN opal? ; 

declaracion : tipodato ID (COMA ID)*;// int x, y, z
            
declaracionArreglos : tipodato ID CA NUMERO CC // char arreglo[] y char arreglo[] (con esto cadenas)
                    | tipodato (MULT) ID;// char *arreglo (ESTE VA A FALLAR EN LA declAsig)

declAsig : declaracion ASIG opal //int x = 3 int x = a
          | declaracionArreglos ASIG COMA opal COMA // char cadena[5] = "c"
          | declaracionArreglos ASIG LLA NUMERO (COMA NUMERO)* LLC // int arreglo = {2,3}
          | declaracion COMA asignacion (COMA opal)* // int x, y=10
          | declaracion ASIG opal COMA asignacion (COMA opal)* // int x=10,y;
          ;

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
          | ID ASIG COMs opal COMs// letra = 'a'
          | ID CA NUMERO CC ASIG COMs opal COMs// cadena[5] = 'a'
          | ID CA NUMERO CC ASIG NUMERO //arreglo[5] = 2
          // | ID opComp ASIG opal //x+=operacion
          | ID ASIG callFunction
          //| incremento
          | decremento
          ;

opal: or;  //completar una operacion aridmeticas, buscar en cppreference, agregamoss operaciones relacionales

or : and (OR and)* ;

and : comp (AND comp)* ;

comp : exp ((MAYOR | MENOR | MENOREQ | MAYOREQ | IGUAL | DIFERENTE) exp)? ;

exp : term ((SUMA | RESTA)term)* ; //e es una expresion prima

term : factor ((MULT | DIV | MOD)factor)*;

// e : SUMA term e // a partir del segundo termino
//   | RESTA term e
//   | //regla vacia 
//   ;

factor : NUMERO  //parentesis es factor
      | ID
      | PA exp PC
      // | LETRA+
      ;

iwhile : WHILE PA opal PC instruccion ;

bloque : LLA instrucciones LLC; 

//for :
ifor : FOR PA init PYC cond PYC iter PC instruccion
    //  | FOR PA declAsig PYC cond PYC iter PC instruccion 
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
iif : IF PA opal PC instruccion ielse
      | IF PA opal PC instruccion
    ; 
ielse : ELSE instruccion;       