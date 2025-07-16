REPORT zexample.

FORM hello_world.
  WRITE 'Hello, world!'.
ENDFORM.

CLASS lcl_example DEFINITION.
  PUBLIC SECTION.
    METHODS: run.
ENDCLASS.

CLASS lcl_example IMPLEMENTATION.
  METHOD run.
    PERFORM hello_world.
  ENDMETHOD.
ENDCLASS.

START-OF-SELECTION.
  DATA(lo_obj) = NEW lcl_example().
  lo_obj->run( ).
