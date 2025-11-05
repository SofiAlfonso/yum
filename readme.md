# Guía de Instalación y Configuración

## Ruta principal

Accede a la aplicación desde la siguiente URL:

    http://127.0.0.1:8000/register/

---

## Pasos para correr el programa

1. **Descargue el proyecto**  
   Descargue el archivo zip del proyecto desde la rama `develop`.

2. **Descomprima el proyecto**  
   Descomprima el zip y ábralo en el editor de su preferencia.

3. **Instale Python y pip**  
   Asegúrese de tener instalado **Python** y **pip**.

4. **Cree un entorno virtual**  
   Abra la terminal (ubicada en la carpeta raíz del proyecto) y ejecute los siguientes comandos (uno por uno):

       python -m venv venv
       venv/Scripts/activate

5. **Active el entorno y seleccione el intérprete correcto**  
   Una vez activado el entorno virtual (`venv`), asegúrese de seleccionar el intérprete correcto en su editor.  
   Luego instale las dependencias con:

       pip install -r requirements.txt

6. **Obtenga una API Key de Google AI Studio**  
   Visite [Google AI Studio](https://aistudio.google.com/prompts/new_chat?_gl=1*ymrbr6*_up*MQ..&gclid=Cj0KCQjwoP_FBhDFARIsANPG24OaVPkhh77e0iNYldQxZ5vza2SXsdf9DUNaCSq46HrSyPxNmJpv9RsaAmosEALw_wcB&gclsrc=aw.ds&gbraid=0AAAAACn9t67CdMAbOMDvJQpXPAMibqShI) y presione **Get started**, luego **Get API Key**, y genere su API Key.  
   Copie el token que obtenga en su portapapeles.

7. **Configure el archivo `.env`**  
   En el proyecto, cree un archivo llamado `.env` en la raíz.  
   Copie el contenido de `example.env` en `.env` y reemplace la frase `aqui_va_tu_api_key` por el token que guardó en el portapapeles.  
   **Guarde los cambios antes de continuar**.

8. **Compile los archivos de idiomas**  
   Ejecute el siguiente comando para preparar el lenguaje de la aplicación:

       python manage.py compilemessages

9. **Ejecute el servidor**  
   Inicie la aplicación con el siguiente comando:

       python manage.py runserver

   Luego ingrese a la ruta principal proporcionada arriba.

---

## Información Adicional

### Cuentas

La ruta principal lo llevará a la página de registro, donde podrá crear un usuario **admin** o **común**.  
Cuando complete el registro, se le redireccionará a la página principal correspondiente (según el tipo de usuario), donde podrá explorar todas las funcionalidades de la aplicación.

> **Tenga presente:**  
> - Si no está autenticado, no podrá ingresar a ninguna vista.  
> - Un usuario común no podrá ingresar a las vistas exclusivas para admin ni viceversa.  
> - Se recomienda crear un usuario por cada rol existente.

---

### Idiomas

El idioma por defecto de la aplicación es **español**.  
Si desea cambiar de idioma puede dirigirse al archivo de configuración:

    yum/yum/settings.py

Busque la línea:

    LANGUAGE_CODE = 'es'

Cambie `'es'` por `'en'` y guarde los cambios.

Al recargar el servidor y volver a ingresar a la aplicación, podrá verla en **inglés**.