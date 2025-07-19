REPORT z_dual_standard_objects.

*----- входные номера материалов и клиентов (по два каждого) -----
DATA lt_matnrs  TYPE STANDARD TABLE OF matnr WITH EMPTY KEY.
DATA lt_kunnrs  TYPE STANDARD TABLE OF kunnr WITH EMPTY KEY.

APPEND '000000000000000001' TO lt_matnrs.
APPEND '000000000000000002' TO lt_matnrs.

APPEND '0000001000' TO lt_kunnrs.
APPEND '0000002000' TO lt_kunnrs.

*----- прямой доступ к стандартным таблицам (MARA, KNA1) ---------
DATA lt_mara TYPE TABLE OF mara.
DATA lt_kna1 TYPE TABLE OF kna1.

SELECT * FROM mara INTO TABLE lt_mara WHERE matnr IN @lt_matnrs UP TO 2 ROWS.
SELECT * FROM kna1 INTO TABLE lt_kna1 WHERE kunnr IN @lt_kunnrs UP TO 2 ROWS.

*----- BAPI 1: детали материалов --------------------------------
DATA lt_mat_desc TYPE TABLE OF bapimatm.

LOOP AT lt_matnrs INTO DATA(lv_matnr).
  CALL FUNCTION 'BAPI_MATERIAL_GET_DETAIL'
    EXPORTING
      material            = lv_matnr
    TABLES
      materialdescription = lt_mat_desc.
ENDLOOP.

*----- BAPI 2: детали клиентов ----------------------------------
DATA lt_cust_data TYPE TABLE OF bapikna1.

LOOP AT lt_kunnrs INTO DATA(lv_kunnr).
  CALL FUNCTION 'BAPI_CUSTOMER_GETDETAIL2'
    EXPORTING
      customerno   = lv_kunnr
    TABLES
      customerdata = lt_cust_data.
ENDLOOP.

*----- Класс 1 (объект 1): ALV материалов -----------------------
DATA(lr_salv_mat) = NEW cl_salv_table( ).
cl_salv_table=>factory(
  IMPORTING r_salv_table = lr_salv_mat
  CHANGING  t_table      = lt_mat_desc ).
lr_salv_mat->display( ).

*----- Класс 1 (объект 2): ALV клиентов -------------------------
DATA(lr_salv_cust) = NEW cl_salv_table( ).
cl_salv_table=>factory(
  IMPORTING r_salv_table = lr_salv_cust
  CHANGING  t_table      = lt_cust_data ).
lr_salv_cust->display( ).

*----- Класс 2 (CL_GUI_FRONTEND_SERVICES) — выгрузка файлов -----
DATA lv_file TYPE string.

cl_gui_frontend_services=>file_save_dialog( CHANGING filename = lv_file ).
IF sy-subrc = 0.
  cl_gui_frontend_services=>gui_download(
      EXPORTING filename = lv_file
                filetype = 'ASC'
      TABLES    data_tab = lt_mat_desc ).
ENDIF.

cl_gui_frontend_services=>file_save_dialog( CHANGING filename = lv_file ).
IF sy-subrc = 0.
  cl_gui_frontend_services=>gui_download(
      EXPORTING filename = lv_file
                filetype = 'ASC'
      TABLES    data_tab = lt_cust_data ).
ENDIF.
