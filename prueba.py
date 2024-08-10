import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select


# Define la carpeta donde se guardarán las capturas de pantalla
screenshot_dir = "screenshots"

# Crea la carpeta si no existe
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


def take_screenshot(test_name):
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Captura guardada en {screenshot_path}")


def wait_and_send_keys(element, keys):
    time.sleep(2)  # Simula un tiempo de espera entre interacciones
    element.send_keys(keys)


# Inicializar el driver (en este caso, Chrome)
driver = webdriver.Chrome()

# Definir URL base
base_url = "http://localhost:5290"  # Cambia esta URL a la de tu aplicación local


# 1. Prueba de Inicio de Sesión
def test_login():
    try:
        driver.get(base_url)

        # Espera hasta que el campo de usuario esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "NombreUsuario"))
        )

        # Introduce el nombre de usuario y la contraseña
        wait_and_send_keys(driver.find_element(By.ID, "NombreUsuario"), "Admin")
        wait_and_send_keys(driver.find_element(By.ID, "Clave"), "123")
        driver.find_element(By.CLASS_NAME, "btn-primary").click()

        print("Inicio de sesión exitoso")
        take_screenshot("test_login")
        return True

    except (NoSuchElementException, TimeoutException):
        print("Error: Inicio de sesión fallido")
        take_screenshot("test_login_fail")
        return False


# 2. Prueba de Creación de Usuario
def test_create_user():
    try:
        driver.get(f"{base_url}/Usuario/Index")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnNuevoUsuario"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtNombreCompleto"))
        )
        wait_and_send_keys(
            driver.find_element(By.ID, "txtNombreCompleto"), "Test123"
        )
        wait_and_send_keys(
            driver.find_element(By.ID, "txtNombreUsuario"), "test prue2"
        )
        wait_and_send_keys(driver.find_element(By.ID, "txtContrasenia"), "1234")
        wait_and_send_keys(driver.find_element(By.ID, "txtRepetirContrasenia"), "1234")
        driver.find_element(By.ID, "btnGuardar").click()

        # Verifica que aparezca el mensaje de éxito
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Usuario registrado!')]")
            )
        )
        
        time.sleep(2)
        print("Creación de usuario exitosa")
        take_screenshot("test_create_user")

    except TimeoutException:
        print("Error: Creación de usuario fallida")
        take_screenshot("test_create_user_fail")


# 3. Prueba de Creación de Estudiante
def test_create_student():
    try:
        driver.get(f"{base_url}/Estudiante/Index")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnNuevoEstudiante"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtNombres"))
        )
        wait_and_send_keys(driver.find_element(By.ID, "txtNombres"), "Rainel")
        wait_and_send_keys(driver.find_element(By.ID, "txtApellidos"), "Olivo")
        driver.find_element(By.ID, "btnGuardar").click()

        # Verifica que el estudiante se haya creado correctamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        search_box = driver.find_element(By.ID, "dt-search-0")
        search_box.clear()
        search_box.send_keys("Rainel Olivo")
        
        time.sleep(2)
        print("Creación de estudiante exitosa")
        take_screenshot("test_create_student")

    except TimeoutException:
        print("Error: Creación de estudiante fallida")
        take_screenshot("test_create_student_fail")


# 4. Prueba de Búsqueda de Estudiante
def test_search_student():
    try:
        driver.get(f"{base_url}/Estudiante/Index")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        wait_and_send_keys(driver.find_element(By.ID, "dt-search-0"), "Juan Pérez")

        # Verifica que el estudiante existe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        search_box = driver.find_element(By.ID, "dt-search-0")
        search_box.clear()
        search_box.send_keys("Juan Pérez")
        
        time.sleep(2)
        print("Búsqueda de estudiante exitosa")
        take_screenshot("test_search_student")

    except TimeoutException:
        print("Error: Búsqueda de estudiante fallida")
        take_screenshot("test_search_student_fail")


# 5. Prueba de Creación de Libro
def test_create_book():
    try:
        driver.get(f"{base_url}/Libro/Index")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnNuevoLibro"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtTitulo"))
        )
        wait_and_send_keys(driver.find_element(By.ID, "txtTitulo"), "Cien años de soledad")
        wait_and_send_keys(driver.find_element(By.ID, "txtAutor"), "Gabriel García Márquez")

        # Selecciona la categoría "Ciencia" del dropdown cboCategoria
        categoria_dropdown = Select(driver.find_element(By.ID, "cboCategoria"))
        categoria_dropdown.select_by_visible_text("Novela")

        wait_and_send_keys(
            driver.find_element(By.ID, "txtFechaPublicacion"), "2024-08-10"
        )
        wait_and_send_keys(driver.find_element(By.ID, "txtCantidad"), "22")
        driver.find_element(By.ID, "btnGuardar").click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Libro registrado!')]")
            )
        )
       
        time.sleep(2)
        print("Creación de libro exitosa")
        take_screenshot("test_create_book")

    except TimeoutException:
        print("Error: Creación de libro fallida")
        take_screenshot("test_create_book_fail")


# 6. Prueba de Búsqueda de Libro
def test_search_book():
    try:
        # Navegar a la página del índice de libros
        driver.get(f"{base_url}/Libro/Index")

        # Esperar hasta que el campo de búsqueda esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )

        # Enviar el nombre del libro en el campo de búsqueda
        wait_and_send_keys(
            driver.find_element(By.ID, "dt-search-0"), "Cien años de soledad"
        )
        
        time.sleep(2)
        print("Búsqueda de libro exitosa")
        take_screenshot("test_search_book")
        
    except TimeoutException:
        print("Error: Búsqueda de libro fallida")
        take_screenshot("test_search_book_fail")


# 7. Prueba de edit studen
def test_edit_student():
    try:
        driver.get(f"{base_url}/Estudiante/Index")

        # Buscar el estudiante en la tabla
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        search_field.send_keys("Rodrigo Mendez")

        # Esperar a que el botón de edición sea clickeable y hacer clic
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.me-1")
            )
        )
        edit_button.click()

        # Esperar a que el formulario de edición sea visible y que el campo sea interactivo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "txtNombres"))
        )

        # Limpiar el campo usando JavaScript
        nombres_field = driver.find_element(By.ID, "txtNombres")
        driver.execute_script("arguments[0].value = '';", nombres_field)
        nombres_field.send_keys("Estudiante Editado")
        
        apellidos_field = driver.find_element(By.ID, "txtApellidos")
        driver.execute_script("arguments[0].value = '';", apellidos_field)
        apellidos_field.send_keys("Apellido Editado")
       
        # Hacer clic en el botón de guardar
        driver.find_element(By.ID, "btnGuardar").click()

        # Verificar que aparezca el mensaje de éxito
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Se guardaron los cambios!')]")
            )
        )
        
        time.sleep(2) 
        print("Edición de estudiante exitosa")
        take_screenshot("test_edit_student")

    except TimeoutException:
        print("Error: Edición de estudiante fallida")
        take_screenshot("test_edit_student_fail")



# 8. Prueba de Devolución de Libro
def test_return_book():
    try:
        driver.get(f"{base_url}/Prestamo/Index")
        
        # Buscar el libro en la tabla de préstamos
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        search_field.send_keys("Psicologia para principiantes")

        # Esperar a que el botón de devolución aparezca y hacer clic
        return_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-primary.me-1")
            )
        )
        return_button.click()

        # Confirmar la devolución en la alerta 
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".swal2-confirm.swal2-styled.swal2-default-outline")
            )
        )
        confirm_button.click()

        # Verificar que aparezca el mensaje de devolución exitosa
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Devuelto!')]")
            )
        )

        time.sleep(2)
        print("Devolución de libro exitosa")
        take_screenshot("test_return_book")
    
    except TimeoutException:
        print("Error: Devolución de libro fallida")
        take_screenshot("test_return_book_fail")


# 9. Prueba de Validación de Dashboard
def test_dashboard():
    try:
        driver.get(f"{base_url}/Home/Index")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mt-4"))
        )
        
        print("Validación del dashboard exitosa")
        take_screenshot("test_dashboard")

    except TimeoutException:
        print("Error: Validación del dashboard fallida")
        take_screenshot("test_dashboard_fail")


# 10. Prueba de eliminar usuario
def test_delete_user():
    try:
        driver.get(f"{base_url}/Usuario/Index")

        # Buscar el usuario en la tabla
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dt-search-0"))
        )
        search_field.send_keys("test prue1")

        # Esperar a que el botón de eliminación aparezca y hacer clic
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-sm.btn-outline-danger.me-1")
            )
        )
        delete_button.click()

        # Confirmar la eliminación en la alerta
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".swal2-confirm.swal2-styled.swal2-default-outline")
            )
        )
        confirm_button.click()

        # Verificar que aparezca el mensaje de éxito de eliminación
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(), 'Eliminado!')]")
            )
        )
        
        time.sleep(2)
        print("Eliminación de usuario exitosa")
        take_screenshot("test_delete_user")

    except TimeoutException:
        print("Error: Eliminación de usuario fallida")
        take_screenshot("test_delete_user_fail")

       

# Ejecutar las pruebas
if test_login():
    test_create_user()
    test_create_student()
    test_search_student()
    test_create_book()
    test_search_book()
    test_edit_student()
    test_return_book()
    test_dashboard()
    test_delete_user()

# Cierra el driver
driver.quit()
