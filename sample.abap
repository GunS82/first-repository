CLASS zcl_my_class DEFINITION.
ENDCLASS.

CLASS zcl_invalid_class DEFINITION.
ENDCLASS.

FUNCTION my_function.
ENDFUNCTION.

FUNCTION bad_function.
ENDFUNCTION.

FORM my_form.
  SELECT * FROM mara INTO TABLE lt_mara.
  SELECT * FROM vbap INTO TABLE lt_vbap.
  SELECT * FROM zinvalid INTO TABLE lt_z.
ENDFORM.
