
"""
Sistema de gestión de clientes, servicios y reservas.
Curso: Programación
Código: 213023
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging


# CONFIGURACIÓN DEL SISTEMA DE REGISTRO

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

# EXCEPCIONES PERSONALIZADAS


class ErrorSistema(Exception):
    """Excepción general del sistema."""


class DatoInvalidoError(ErrorSistema):
    """Error cuando un dato no cumple las condiciones."""


class ServicioNoDisponibleError(ErrorSistema):
    """Error cuando un servicio no está disponible."""


class ReservaInvalidaError(ErrorSistema):
    """Error cuando una reserva no es válida."""


class OperacionNoPermitidaError(ErrorSistema):
    """Error cuando se intenta una operación no permitida."""



# CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):

    def __init__(self, identificador):

        if not identificador or not identificador.strip():
            raise DatoInvalidoError(
                "El identificador no puede estar vacío."
            )

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass



# CLASE CLIENTE

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):

        super().__init__(identificador)

        if not nombre or len(nombre.strip()) < 3:
            raise DatoInvalidoError(
                "El nombre debe tener mínimo 3 caracteres."
            )

        if (
            not correo
            or "@" not in correo
            or "." not in correo.split("@")[-1]
        ):
            raise DatoInvalidoError(
                "El correo electrónico no es válido."
            )

        if (
            not telefono
            or not telefono.isdigit()
            or len(telefono) < 7
        ):
            raise DatoInvalidoError(
                "El teléfono debe tener mínimo 7 dígitos."
            )

        # Atributos privados para aplicar encapsulación.
        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono.strip()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):

        return (
            f"Cliente: {self.__nombre} | "
            f"ID: {self.identificador} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )


# CLASE ABSTRACTA SERVICIO

class Servicio(Entidad, ABC):

    def __init__(self, identificador, nombre, tarifa_hora):

        super().__init__(identificador)

        if not nombre or not nombre.strip():
            raise DatoInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        if (
            not isinstance(tarifa_hora, (int, float))
            or isinstance(tarifa_hora, bool)
            or tarifa_hora <= 0
        ):
            raise DatoInvalidoError(
                "La tarifa debe ser mayor que cero."
            )

        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar_horas(self, horas):

        if (
            not isinstance(horas, (int, float))
            or isinstance(horas, bool)
            or horas <= 0
        ):
            raise DatoInvalidoError(
                "Las horas deben ser mayores que cero."
            )

    def cambiar_disponibilidad(self, disponible):

        if not isinstance(disponible, bool):
            raise DatoInvalidoError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        self.disponible = disponible


# SERVICIO DE RESERVA DE SALAS

class ServicioSala(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_hora,
        capacidad
    ):

        super().__init__(
            identificador,
            nombre,
            tarifa_hora
        )

        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError(
                "La capacidad debe ser un entero positivo."
            )

        self.capacidad = capacidad

    def calcular_costo(
        self,
        horas,
        impuesto=0,
        descuento=0
    ):

        self.validar_horas(horas)

        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("Impuesto inválido.")

        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("Descuento inválido.")

        subtotal = self.tarifa_hora * horas

        return subtotal * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_hora:,.0f}"
        )


# SERVICIO DE ALQUILER DE EQUIPOS

class ServicioEquipo(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_hora,
        tipo_equipo
    ):

        super().__init__(
            identificador,
            nombre,
            tarifa_hora
        )

        if not tipo_equipo or not tipo_equipo.strip():
            raise DatoInvalidoError(
                "Debe indicar el tipo de equipo."
            )

        self.tipo_equipo = tipo_equipo.strip()

    def calcular_costo(
        self,
        horas,
        impuesto=0,
        descuento=0
    ):

        self.validar_horas(horas)

        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("Impuesto inválido.")

        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("Descuento inválido.")

        subtotal = self.tarifa_hora * horas

        return subtotal * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Equipo: {self.nombre} | "
            f"Tipo: {self.tipo_equipo} | "
            f"Tarifa por hora: ${self.tarifa_hora:,.0f}"
        )



# SERVICIO DE ASESORÍAS

class ServicioAsesoria(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        tarifa_hora,
        especialidad
    ):

        super().__init__(
            identificador,
            nombre,
            tarifa_hora
        )

        if not especialidad or not especialidad.strip():
            raise DatoInvalidoError(
                "Debe indicar la especialidad."
            )

        self.especialidad = especialidad.strip()

    def calcular_costo(
        self,
        horas,
        impuesto=0,
        descuento=0
    ):

        self.validar_horas(horas)

        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("Impuesto inválido.")

        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("Descuento inválido.")

        subtotal = self.tarifa_hora * horas

        return subtotal * (1 - descuento) * (1 + impuesto)

    def describir(self):

        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self.especialidad} | "
            f"Tarifa por hora: ${self.tarifa_hora:,.0f}"
        )


# CLASE RESERVA

class Reserva(Entidad):

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        horas
    ):

        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente inválido.")

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio inválido.")

        servicio.validar_horas(horas)

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no está disponible."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.horas = float(horas)
        self.estado = "Pendiente"
        self.fecha = datetime.now()

    def confirmar(self):

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio ya no está disponible."
            )

        self.estado = "Confirmada"

        logging.info(
            "Reserva %s confirmada.",
            self.identificador
        )

    def cancelar(self):

        if self.estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar esta reserva."
            )

        self.estado = "Cancelada"

        logging.info(
            "Reserva %s cancelada.",
            self.identificador
        )

    def procesar(self, impuesto=0, descuento=0):

        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada."
            )

        try:

            total = self.servicio.calcular_costo(
                self.horas,
                impuesto,
                descuento
            )

        except Exception as error:

            logging.exception(
                "Error procesando reserva %s.",
                self.identificador
            )

            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

        else:

            self.estado = "Procesada"

            logging.info(
                "Reserva %s procesada. Total: %.2f",
                self.identificador,
                total
            )

            return total

        finally:

            logging.info(
                "Finalizó el procesamiento de reserva %s.",
                self.identificador
            )

    def describir(self):

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Horas: {self.horas} | "
            f"Estado: {self.estado}"
        )


# SISTEMA PRINCIPAL SOFTWARE FJ

class SistemaSoftwareFJ:

    def __init__(self):

        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):

        if any(
            c.identificador == cliente.identificador
            for c in self.clientes
        ):
            raise DatoInvalidoError(
                "El cliente ya está registrado."
            )

        self.clientes.append(cliente)

        logging.info(
            "Cliente registrado: %s",
            cliente.identificador
        )

        return cliente

    def registrar_servicio(self, servicio):

        if any(
            s.identificador == servicio.identificador
            for s in self.servicios
        ):
            raise DatoInvalidoError(
                "El servicio ya está registrado."
            )

        self.servicios.append(servicio)

        logging.info(
            "Servicio registrado: %s",
            servicio.identificador
        )

        return servicio

    def crear_reserva(
        self,
        identificador,
        id_cliente,
        id_servicio,
        horas
    ):

        cliente = next(
            (
                c for c in self.clientes
                if c.identificador == id_cliente
            ),
            None
        )

        servicio = next(
            (
                s for s in self.servicios
                if s.identificador == id_servicio
            ),
            None
        )

        if cliente is None:
            raise DatoInvalidoError(
                "No se encontró el cliente."
            )

        if servicio is None:
            raise DatoInvalidoError(
                "No se encontró el servicio."
            )

        if any(
            r.identificador == identificador
            for r in self.reservas
        ):
            raise DatoInvalidoError(
                "El identificador de reserva ya existe."
            )

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            horas
        )

        self.reservas.append(reserva)

        logging.info(
            "Reserva creada: %s",
            identificador
        )

        return reserva

    def buscar_reserva(self, identificador):

        reserva = next(
            (
                r for r in self.reservas
                if r.identificador == identificador
            ),
            None
        )

        if reserva is None:
            raise DatoInvalidoError(
                "No se encontró la reserva."
            )

        return reserva

    def listar_clientes(self):

        print("\n========== CLIENTES ==========")

        for cliente in self.clientes:
            print(cliente.describir())

        if not self.clientes:
            print("No hay clientes registrados.")

    def listar_servicios(self):

        print("\n========== SERVICIOS ==========")

        for servicio in self.servicios:

            disponibilidad = (
                "Disponible"
                if servicio.disponible
                else "No disponible"
            )

            print(
                servicio.describir(),
                "|",
                disponibilidad
            )

        if not self.servicios:
            print("No hay servicios registrados.")

    def listar_reservas(self):

        print("\n========== RESERVAS ==========")

        for reserva in self.reservas:
            print(reserva.describir())

        if not self.reservas:
            print("No hay reservas registradas.")


# PRUEBAS AUTOMÁTICAS

def ejecutar_pruebas():

    sistema = SistemaSoftwareFJ()

    print("\n========================================")
    print("       SOFTWARE FJ - PRUEBAS")
    print("========================================")

    contador = 0

    def ejecutar(numero, descripcion, accion):

        nonlocal contador
        contador += 1

        print(f"\n{numero}. {descripcion}")

        try:

            resultado = accion()

            print("Resultado:", resultado if resultado is not None
                  else "Operación realizada correctamente.")

        except ErrorSistema as error:

            logging.exception(
                "Error controlado en operación %s",
                numero
            )

            print("Error controlado:", error)

        except (ValueError, TypeError) as error:

            logging.exception(
                "Error de datos en operación %s",
                numero
            )

            print("Error de datos:", error)

        except Exception as error:

            logging.exception(
                "Error inesperado en operación %s",
                numero
            )

            print("Error inesperado controlado:", error)

    # Operación 1
    ejecutar(
        1,
        "Registrar cliente Ana",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C001",
                "Ana Pérez",
                "ana@email.com",
                "3001234567"
            )
        ).describir()
    )

    # Operación 2
    ejecutar(
        2,
        "Registrar cliente Carlos",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C002",
                "Carlos Gómez",
                "carlos@email.com",
                "3107654321"
            )
        ).describir()
    )

    # Operación 3
    ejecutar(
        3,
        "Registrar cliente con correo inválido",
        lambda: sistema.registrar_cliente(
            Cliente(
                "C003",
                "Luis Díaz",
                "correo-invalido",
                "3001112233"
            )
        )
    )

    # Operación 4
    ejecutar(
        4,
        "Registrar sala",
        lambda: sistema.registrar_servicio(
            ServicioSala(
                "S001",
                "Sala de reuniones",
                50000,
                20
            )
        ).describir()
    )

    # Operación 5
    ejecutar(
        5,
        "Registrar equipo",
        lambda: sistema.registrar_servicio(
            ServicioEquipo(
                "S002",
                "Portátil",
                15000,
                "Computador"
            )
        ).describir()
    )

    # Operación 6
    ejecutar(
        6,
        "Registrar asesoría",
        lambda: sistema.registrar_servicio(
            ServicioAsesoria(
                "S003",
                "Asesoría de software",
                70000,
                "Desarrollo de software"
            )
        ).describir()
    )

    # Operación 7
    ejecutar(
        7,
        "Registrar servicio con tarifa negativa",
        lambda: sistema.registrar_servicio(
            ServicioSala(
                "S004",
                "Sala inválida",
                -1000,
                10
            )
        )
    )

    # Operación 8
    ejecutar(
        8,
        "Crear reserva R001",
        lambda: sistema.crear_reserva(
            "R001",
            "C001",
            "S001",
            2
        ).describir()
    )

    # Operación 9
    ejecutar(
        9,
        "Confirmar reserva R001",
        lambda: sistema.buscar_reserva(
            "R001"
        ).confirmar()
    )

    # Operación 10
    ejecutar(
        10,
        "Procesar reserva R001 con impuesto del 19%",
        lambda: (
            f"Total: ${sistema.buscar_reserva('R001').procesar(0.19):,.0f}"
        )
    )

    # Operación 11
    ejecutar(
        11,
        "Cancelar reserva ya procesada",
        lambda: sistema.buscar_reserva(
            "R001"
        ).cancelar()
    )

    # Operación 12
    ejecutar(
        12,
        "Reservar servicio inexistente",
        lambda: sistema.crear_reserva(
            "R002",
            "C001",
            "S999",
            1
        )
    )

    # Operación 13
    ejecutar(
        13,
        "Crear reserva con cero horas",
        lambda: sistema.crear_reserva(
            "R003",
            "C002",
            "S002",
            0
        )
    )

    # Operación 14
    ejecutar(
        14,
        "Crear reserva R004",
        lambda: sistema.crear_reserva(
            "R004",
            "C002",
            "S003",
            1
        ).describir()
    )

    # Operación 15
    ejecutar(
        15,
        "Cancelar reserva R004",
        lambda: sistema.buscar_reserva(
            "R004"
        ).cancelar()
    )

    # Operación 16
    ejecutar(
        16,
        "Procesar reserva cancelada",
        lambda: sistema.buscar_reserva(
            "R004"
        ).procesar()
    )

    # Operación 17
    def probar_servicio_no_disponible():

        servicio = next(
            s for s in sistema.servicios
            if s.identificador == "S002"
        )

        servicio.cambiar_disponibilidad(False)

        try:

            return sistema.crear_reserva(
                "R005",
                "C001",
                "S002",
                1
            )

        finally:

            servicio.cambiar_disponibilidad(True)

    ejecutar(
        17,
        "Reservar servicio no disponible",
        probar_servicio_no_disponible
    )

    # Operación 18
    ejecutar(
        18,
        "Calcular costo con descuento e impuesto",
        lambda: (
            f"Total: ${sistema.servicios[1].calcular_costo(2, 0.19, 0.10):,.0f}"
        )
    )

    print("\n========================================")
    print("TOTAL DE OPERACIONES:", contador)
    print("========================================")

    sistema.listar_clientes()
    sistema.listar_servicios()
    sistema.listar_reservas()

    print("\nLos registros se guardaron en logs.txt.")



# MENÚ INTERACTIVO

def menu_interactivo():

    sistema = SistemaSoftwareFJ()

    while True:

        print("\n========== SOFTWARE FJ ==========")
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Confirmar reserva")
        print("5. Cancelar reserva")
        print("6. Procesar reserva")
        print("7. Listar clientes")
        print("8. Listar servicios")
        print("9. Listar reservas")
        print("0. Salir")

        try:

            opcion = input(
                "Seleccione una opción: "
            ).strip()

            if opcion == "1":

                cliente = Cliente(
                    input("Identificación: "),
                    input("Nombre: "),
                    input("Correo: "),
                    input("Teléfono: ")
                )

                sistema.registrar_cliente(cliente)

                print("Cliente registrado correctamente.")

            elif opcion == "2":

                print("\nTipos de servicio:")
                print("1. Reserva de salas")
                print("2. Alquiler de equipos")
                print("3. Asesorías")

                tipo = input("Seleccione el tipo: ").strip()

                identificador = input("ID del servicio: ")
                nombre = input("Nombre: ")

                tarifa = float(
                    input("Tarifa por hora: $")
                )

                if tipo == "1":

                    capacidad = int(
                        input("Capacidad de personas: ")
                    )

                    servicio = ServicioSala(
                        identificador,
                        nombre,
                        tarifa,
                        capacidad
                    )

                elif tipo == "2":

                    equipo = input("Tipo de equipo: ")

                    servicio = ServicioEquipo(
                        identificador,
                        nombre,
                        tarifa,
                        equipo
                    )

                elif tipo == "3":

                    especialidad = input("Especialidad: ")

                    servicio = ServicioAsesoria(
                        identificador,
                        nombre,
                        tarifa,
                        especialidad
                    )

                else:

                    raise DatoInvalidoError(
                        "Tipo de servicio no válido."
                    )

                sistema.registrar_servicio(servicio)

                print("Servicio registrado correctamente.")

            elif opcion == "3":

                reserva = sistema.crear_reserva(
                    input("ID de reserva: "),
                    input("ID del cliente: "),
                    input("ID del servicio: "),
                    float(input("Cantidad de horas: "))
                )

                print(reserva.describir())

            elif opcion == "4":

                reserva = sistema.buscar_reserva(
                    input("ID de reserva: ")
                )

                reserva.confirmar()

                print("Reserva confirmada.")

            elif opcion == "5":

                reserva = sistema.buscar_reserva(
                    input("ID de reserva: ")
                )

                reserva.cancelar()

                print("Reserva cancelada.")

            elif opcion == "6":

                reserva = sistema.buscar_reserva(
                    input("ID de reserva: ")
                )

                impuesto = float(
                    input("Impuesto (ejemplo 0.19): ")
                )

                descuento = float(
                    input("Descuento (ejemplo 0.10): ")
                )

                total = reserva.procesar(
                    impuesto,
                    descuento
                )

                print(
                    f"Reserva procesada. Total: ${total:,.0f}"
                )

            elif opcion == "7":

                sistema.listar_clientes()

            elif opcion == "8":

                sistema.listar_servicios()

            elif opcion == "9":

                sistema.listar_reservas()

            elif opcion == "0":

                print("Gracias por utilizar Software FJ.")
                break

            else:

                raise DatoInvalidoError(
                    "Seleccione una opción entre 0 y 9."
                )

        except ErrorSistema as error:

            logging.exception("Error controlado en el menú.")

            print("No se pudo completar la operación:", error)

        except (ValueError, TypeError) as error:

            logging.exception("Error de entrada en el menú.")

            print("Verifique los datos ingresados:", error)

        except Exception as error:

            logging.exception("Error inesperado en el menú.")

            print("Se presentó un error inesperado:", error)



# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":

    print("\n========================================")
    print("       SISTEMA SOFTWARE FJ")
    print("========================================")

    print("1. Ejecutar pruebas automáticas")
    print("2. Iniciar menú interactivo")

    try:

        modo = input(
            "Seleccione el modo de ejecución: "
        ).strip()

        if modo == "1":

            ejecutar_pruebas()

        elif modo == "2":

            menu_interactivo()

        else:

            print("Opción no válida.")

    except KeyboardInterrupt:

        logging.warning(
            "Programa interrumpido por el usuario."
        )

        print("\nPrograma interrumpido de forma segura.")

    except Exception as error:

        logging.exception(
            "Error general del programa."
        )

        print("El sistema controló un error:", error)
