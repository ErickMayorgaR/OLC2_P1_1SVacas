
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'initleftORleftANDrightNOTleftIGUALIGUALDIFERENTEMENORMENORIGUALMAYORMAYORIGUALleftMASMENOSleftPORDIVPORCENTAJEleftPARIPARDnonassocPOTENCIArightUMENOSAND ANY BOOLEAN CADENA COMA DECIMAL DIFERENTE DIV DPUNTOS ENTERO ID IGUAL IGUALIGUAL LLAVEDER LLAVEIZQ MAS MAYOR MAYORIGUAL MENOR MENORIGUAL MENOS NOT NUMBER OR PARD PARI POR PORCENTAJE POTENCIA PTCOMA PUNTO RBREAK RCONSOLE RCONTINUE RELSE RFALSE RFUNCTION RIF RLET RLOG RRETURN RTRUE STRINGinit : instruccionesinstrucciones    : instrucciones instruccioninstrucciones : instruccioninstruccion : imprimir PTCOMA\n                    | declaracion_normal PTCOMA\n                    | asignacion_normal PTCOMA\n                    | condicional_if PTCOMA\n                    | funcion PTCOMA\n                    | llamada_funcion PTCOMA\n                    | inst_return PTCOMA\n                    | inst_break PTCOMA\n                    | inst_continue PTCOMAfuncion : RFUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER\n                | RFUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDERllamada_funcion : ID PARI PARD\n                        | ID PARI parametros_ll PARDparametros : parametros COMA parametroparametros : parametroparametro : RLET ID DPUNTOS tipo  \n                | ID DPUNTOS tipo\n                | IDparametros_ll : parametros_ll COMA parametro_llparametros_ll : parametro_llparametro_ll : expresionimprimir : RCONSOLE PUNTO RLOG PARI expresiones_coma PARDdeclaracion_normal : RLET ID DPUNTOS tipo IGUAL expresiondeclaracion_normal : RLET ID IGUAL expresiondeclaracion_normal : RLET IDdeclaracion_normal : RLET ID DPUNTOS tipoasignacion_normal : ID IGUAL expresion DPUNTOS DPUNTOS tipoasignacion_normal : ID IGUAL expresioninst_return : RRETURN expresioninst_return : RRETURNinst_break : RBREAKinst_continue : RCONTINUEcondicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDERcondicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifs RELSE LLAVEIZQ instrucciones LLAVEDERcondicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifscondicional_if : RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE LLAVEIZQ instrucciones LLAVEDERcondicional_elseifs : condicional_elseifs condicional_elseifcondicional_elseifs : condicional_elseifcondicional_elseif : RELSE RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDERtipo : STRING\n            | NUMBER\n            | BOOLEANexpresion : expresion MAS expresion\n                | expresion MENOS expresion\n                | expresion POR expresion\n                | expresion DIV expresion\n                | expresion POTENCIA expresion\n                | expresion PORCENTAJE expresionexpresion : expresion IGUALIGUAL expresion\n                 | expresion DIFERENTE expresion\n                 | expresion MENOR expresion\n                 | expresion MAYOR expresion\n                 | expresion MENORIGUAL expresion\n                 | expresion MAYORIGUAL expresionexpresion : expresion AND expresion\n                 | expresion OR expresionexpresion : MENOS expresion %prec UMENOSexpresion : ENTEROexpresion : DECIMALexpresion : CADENAexpresion : RTRUE\n                | RFALSEexpresion : IDexpresiones_coma : expresiones_coma COMA expresionexpresiones_coma : expresion'
    
_lr_action_items = {'RCONSOLE':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,132,133,135,136,141,142,],[13,13,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,13,13,13,13,13,13,13,13,13,13,13,13,]),'RLET':([0,2,3,21,22,23,24,25,26,27,28,29,30,54,104,106,108,114,116,117,123,132,133,135,136,141,142,],[14,14,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,84,14,14,84,14,14,14,14,14,14,14,14,14,14,]),'ID':([0,2,3,14,17,18,21,22,23,24,25,26,27,28,29,30,33,34,35,38,47,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,84,101,104,106,108,111,114,116,117,123,132,133,134,135,136,141,142,],[15,15,-3,32,36,44,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,44,44,44,44,44,80,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,109,44,15,15,80,44,15,15,15,15,15,15,44,15,15,15,15,]),'RIF':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,126,129,132,133,135,136,141,142,],[16,16,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,16,16,16,16,16,16,131,131,16,16,16,16,16,16,]),'RFUNCTION':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,132,133,135,136,141,142,],[17,17,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,17,17,17,17,17,17,17,17,17,17,17,17,]),'RRETURN':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,132,133,135,136,141,142,],[18,18,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,18,18,18,18,18,18,18,18,18,18,18,18,]),'RBREAK':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,132,133,135,136,141,142,],[19,19,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,19,19,19,19,19,19,19,19,19,19,19,19,]),'RCONTINUE':([0,2,3,21,22,23,24,25,26,27,28,29,30,104,106,114,116,117,123,132,133,135,136,141,142,],[20,20,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,20,20,20,20,20,20,20,20,20,20,20,20,]),'$end':([1,2,3,21,22,23,24,25,26,27,28,29,30,],[0,-1,-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,]),'LLAVEDER':([3,21,22,23,24,25,26,27,28,29,30,114,116,123,135,136,142,],[-3,-2,-4,-5,-6,-7,-8,-9,-10,-11,-12,121,122,128,138,139,143,]),'PTCOMA':([4,5,6,7,8,9,10,11,12,18,19,20,32,37,39,40,41,42,43,44,48,49,69,71,72,73,74,75,77,85,86,87,88,89,90,91,92,93,94,95,96,97,98,110,112,113,121,122,125,127,128,130,138,139,143,],[22,23,24,25,26,27,28,29,30,-33,-34,-35,-28,-32,-61,-62,-63,-64,-65,-66,-31,-15,-60,-29,-43,-44,-45,-27,-16,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-25,-26,-30,-36,-13,-38,-41,-14,-40,-39,-37,-42,]),'PUNTO':([13,],[31,]),'IGUAL':([15,32,71,72,73,74,],[33,47,101,-43,-44,-45,]),'PARI':([15,16,36,45,131,],[34,35,54,70,134,]),'MENOS':([18,33,34,35,37,38,39,40,41,42,43,44,47,48,52,53,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,75,78,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,101,111,112,120,134,137,],[38,38,38,38,56,38,-61,-62,-63,-64,-65,-66,38,56,56,56,38,38,38,38,38,38,38,38,38,38,38,38,38,38,-60,38,56,38,-46,-47,-48,-49,-50,-51,56,56,56,56,56,56,56,56,56,38,38,56,56,38,56,]),'ENTERO':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'DECIMAL':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'CADENA':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'RTRUE':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,]),'RFALSE':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'RLOG':([31,],[45,]),'DPUNTOS':([32,39,40,41,42,43,44,48,69,76,80,85,86,87,88,89,90,91,92,93,94,95,96,97,98,109,],[46,-61,-62,-63,-64,-65,-66,76,-60,102,105,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,119,]),'PARD':([34,39,40,41,42,43,44,50,51,52,53,54,69,72,73,74,80,82,83,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,115,118,120,124,137,],[49,-61,-62,-63,-64,-65,-66,77,-23,-24,79,81,-60,-43,-44,-45,-21,107,-18,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,110,-68,-22,-20,-17,-67,-19,140,]),'MAS':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[55,-61,-62,-63,-64,-65,-66,55,55,55,-60,55,-46,-47,-48,-49,-50,-51,55,55,55,55,55,55,55,55,55,55,55,55,]),'POR':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[57,-61,-62,-63,-64,-65,-66,57,57,57,-60,57,57,57,-48,-49,-50,-51,57,57,57,57,57,57,57,57,57,57,57,57,]),'DIV':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[58,-61,-62,-63,-64,-65,-66,58,58,58,-60,58,58,58,-48,-49,-50,-51,58,58,58,58,58,58,58,58,58,58,58,58,]),'POTENCIA':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[59,-61,-62,-63,-64,-65,-66,59,59,59,-60,59,59,59,59,59,None,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'PORCENTAJE':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[60,-61,-62,-63,-64,-65,-66,60,60,60,-60,60,60,60,-48,-49,-50,-51,60,60,60,60,60,60,60,60,60,60,60,60,]),'IGUALIGUAL':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[61,-61,-62,-63,-64,-65,-66,61,61,61,-60,61,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,61,61,61,61,61,61,]),'DIFERENTE':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[62,-61,-62,-63,-64,-65,-66,62,62,62,-60,62,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,62,62,62,62,62,62,]),'MENOR':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[63,-61,-62,-63,-64,-65,-66,63,63,63,-60,63,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,63,63,63,63,63,63,]),'MAYOR':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[64,-61,-62,-63,-64,-65,-66,64,64,64,-60,64,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,64,64,64,64,64,64,]),'MENORIGUAL':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[65,-61,-62,-63,-64,-65,-66,65,65,65,-60,65,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,65,65,65,65,65,65,]),'MAYORIGUAL':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[66,-61,-62,-63,-64,-65,-66,66,66,66,-60,66,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,66,66,66,66,66,66,]),'AND':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[67,-61,-62,-63,-64,-65,-66,67,67,67,-60,67,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,67,67,67,67,67,]),'OR':([37,39,40,41,42,43,44,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,112,120,137,],[68,-61,-62,-63,-64,-65,-66,68,68,68,-60,68,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,68,68,68,68,]),'COMA':([39,40,41,42,43,44,50,51,52,69,72,73,74,80,82,83,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,115,118,120,124,],[-61,-62,-63,-64,-65,-66,78,-23,-24,-60,-43,-44,-45,-21,108,-18,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,111,-68,-22,-20,-17,-67,-19,]),'STRING':([46,102,105,119,],[72,72,72,72,]),'NUMBER':([46,102,105,119,],[73,73,73,73,]),'BOOLEAN':([46,102,105,119,],[74,74,74,74,]),'LLAVEIZQ':([79,81,107,126,129,140,],[104,106,117,132,133,141,]),'RELSE':([121,125,127,130,143,],[126,129,-41,-40,-42,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'init':([0,],[1,]),'instrucciones':([0,104,106,117,132,133,141,],[2,114,116,123,135,136,142,]),'instruccion':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[3,21,3,3,21,21,3,21,3,3,21,21,3,21,]),'imprimir':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,]),'declaracion_normal':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,]),'asignacion_normal':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'condicional_if':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'funcion':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,]),'llamada_funcion':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[9,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'inst_return':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'inst_break':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'inst_continue':([0,2,104,106,114,116,117,123,132,133,135,136,141,142,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,]),'expresion':([18,33,34,35,38,47,55,56,57,58,59,60,61,62,63,64,65,66,67,68,70,78,101,111,134,],[37,48,52,53,69,75,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,52,112,120,137,]),'parametros_ll':([34,],[50,]),'parametro_ll':([34,78,],[51,103,]),'tipo':([46,102,105,119,],[71,113,115,124,]),'parametros':([54,],[82,]),'parametro':([54,108,],[83,118,]),'expresiones_coma':([70,],[99,]),'condicional_elseifs':([121,],[125,]),'condicional_elseif':([121,125,],[127,130,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> init","S'",1,None,None,None),
  ('init -> instrucciones','init',1,'p_inicio','Analizador_Sintactico.py',46),
  ('instrucciones -> instrucciones instruccion','instrucciones',2,'p_instrucciones_lista','Analizador_Sintactico.py',51),
  ('instrucciones -> instruccion','instrucciones',1,'p_instrucciones_2','Analizador_Sintactico.py',57),
  ('instruccion -> imprimir PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',65),
  ('instruccion -> declaracion_normal PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',66),
  ('instruccion -> asignacion_normal PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',67),
  ('instruccion -> condicional_if PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',68),
  ('instruccion -> funcion PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',69),
  ('instruccion -> llamada_funcion PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',70),
  ('instruccion -> inst_return PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',71),
  ('instruccion -> inst_break PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',72),
  ('instruccion -> inst_continue PTCOMA','instruccion',2,'p_instrucciones_evaluar','Analizador_Sintactico.py',73),
  ('funcion -> RFUNCTION ID PARI PARD LLAVEIZQ instrucciones LLAVEDER','funcion',7,'p_funcion','Analizador_Sintactico.py',83),
  ('funcion -> RFUNCTION ID PARI parametros PARD LLAVEIZQ instrucciones LLAVEDER','funcion',8,'p_funcion','Analizador_Sintactico.py',84),
  ('llamada_funcion -> ID PARI PARD','llamada_funcion',3,'p_llamada_funcion','Analizador_Sintactico.py',92),
  ('llamada_funcion -> ID PARI parametros_ll PARD','llamada_funcion',4,'p_llamada_funcion','Analizador_Sintactico.py',93),
  ('parametros -> parametros COMA parametro','parametros',3,'p_parametros','Analizador_Sintactico.py',102),
  ('parametros -> parametro','parametros',1,'p_parametros_2','Analizador_Sintactico.py',107),
  ('parametro -> RLET ID DPUNTOS tipo','parametro',4,'p_parametro','Analizador_Sintactico.py',112),
  ('parametro -> ID DPUNTOS tipo','parametro',3,'p_parametro','Analizador_Sintactico.py',113),
  ('parametro -> ID','parametro',1,'p_parametro','Analizador_Sintactico.py',114),
  ('parametros_ll -> parametros_ll COMA parametro_ll','parametros_ll',3,'p_parametros_ll','Analizador_Sintactico.py',124),
  ('parametros_ll -> parametro_ll','parametros_ll',1,'p_parametros_ll_2','Analizador_Sintactico.py',129),
  ('parametro_ll -> expresion','parametro_ll',1,'p_parametro_ll','Analizador_Sintactico.py',133),
  ('imprimir -> RCONSOLE PUNTO RLOG PARI expresiones_coma PARD','imprimir',6,'p_imprimir','Analizador_Sintactico.py',138),
  ('declaracion_normal -> RLET ID DPUNTOS tipo IGUAL expresion','declaracion_normal',6,'p_declaracion_normal','Analizador_Sintactico.py',143),
  ('declaracion_normal -> RLET ID IGUAL expresion','declaracion_normal',4,'p_declaracion_sin_tipo','Analizador_Sintactico.py',147),
  ('declaracion_normal -> RLET ID','declaracion_normal',2,'p_declaracion_sin_tipo_sin_valor','Analizador_Sintactico.py',151),
  ('declaracion_normal -> RLET ID DPUNTOS tipo','declaracion_normal',4,'p_declaracion_sin_valor','Analizador_Sintactico.py',155),
  ('asignacion_normal -> ID IGUAL expresion DPUNTOS DPUNTOS tipo','asignacion_normal',6,'p_asignacion_var_tipo','Analizador_Sintactico.py',165),
  ('asignacion_normal -> ID IGUAL expresion','asignacion_normal',3,'p_asignacion_var','Analizador_Sintactico.py',169),
  ('inst_return -> RRETURN expresion','inst_return',2,'p_return_expresion','Analizador_Sintactico.py',177),
  ('inst_return -> RRETURN','inst_return',1,'p_return','Analizador_Sintactico.py',181),
  ('inst_break -> RBREAK','inst_break',1,'p_sentencia_transferencia_break','Analizador_Sintactico.py',185),
  ('inst_continue -> RCONTINUE','inst_continue',1,'p_sentencia_transferencia_continue','Analizador_Sintactico.py',189),
  ('condicional_if -> RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER','condicional_if',7,'p_condicional_if','Analizador_Sintactico.py',194),
  ('condicional_if -> RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifs RELSE LLAVEIZQ instrucciones LLAVEDER','condicional_if',12,'p_condicional_if_elseif_else','Analizador_Sintactico.py',198),
  ('condicional_if -> RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER condicional_elseifs','condicional_if',8,'p_condicional_if_elseif','Analizador_Sintactico.py',202),
  ('condicional_if -> RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER RELSE LLAVEIZQ instrucciones LLAVEDER','condicional_if',11,'p_condicional_if_else','Analizador_Sintactico.py',206),
  ('condicional_elseifs -> condicional_elseifs condicional_elseif','condicional_elseifs',2,'p_elseifs_elseifs_elseif','Analizador_Sintactico.py',210),
  ('condicional_elseifs -> condicional_elseif','condicional_elseifs',1,'p_elseifs_elseif','Analizador_Sintactico.py',216),
  ('condicional_elseif -> RELSE RIF PARI expresion PARD LLAVEIZQ instrucciones LLAVEDER','condicional_elseif',8,'p_condicional_elseif','Analizador_Sintactico.py',223),
  ('tipo -> STRING','tipo',1,'p_tipo','Analizador_Sintactico.py',234),
  ('tipo -> NUMBER','tipo',1,'p_tipo','Analizador_Sintactico.py',235),
  ('tipo -> BOOLEAN','tipo',1,'p_tipo','Analizador_Sintactico.py',236),
  ('expresion -> expresion MAS expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',241),
  ('expresion -> expresion MENOS expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',242),
  ('expresion -> expresion POR expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',243),
  ('expresion -> expresion DIV expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',244),
  ('expresion -> expresion POTENCIA expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',245),
  ('expresion -> expresion PORCENTAJE expresion','expresion',3,'p_expresion_binaria','Analizador_Sintactico.py',246),
  ('expresion -> expresion IGUALIGUAL expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',261),
  ('expresion -> expresion DIFERENTE expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',262),
  ('expresion -> expresion MENOR expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',263),
  ('expresion -> expresion MAYOR expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',264),
  ('expresion -> expresion MENORIGUAL expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',265),
  ('expresion -> expresion MAYORIGUAL expresion','expresion',3,'p_expresion_binaria_relacional','Analizador_Sintactico.py',266),
  ('expresion -> expresion AND expresion','expresion',3,'p_expresion_binaria_logica','Analizador_Sintactico.py',282),
  ('expresion -> expresion OR expresion','expresion',3,'p_expresion_binaria_logica','Analizador_Sintactico.py',283),
  ('expresion -> MENOS expresion','expresion',2,'p_expresion_unaria','Analizador_Sintactico.py',301),
  ('expresion -> ENTERO','expresion',1,'p_expresion_entero','Analizador_Sintactico.py',305),
  ('expresion -> DECIMAL','expresion',1,'p_expresion_decimal','Analizador_Sintactico.py',309),
  ('expresion -> CADENA','expresion',1,'p_expresion_cadena','Analizador_Sintactico.py',313),
  ('expresion -> RTRUE','expresion',1,'p_expresion_boolean','Analizador_Sintactico.py',317),
  ('expresion -> RFALSE','expresion',1,'p_expresion_boolean','Analizador_Sintactico.py',318),
  ('expresion -> ID','expresion',1,'p_expresion_identificador','Analizador_Sintactico.py',326),
  ('expresiones_coma -> expresiones_coma COMA expresion','expresiones_coma',3,'p_expresiones_coma_expresiones_coma_expresion','Analizador_Sintactico.py',331),
  ('expresiones_coma -> expresion','expresiones_coma',1,'p_expresiones_coma_expresion','Analizador_Sintactico.py',336),
]
