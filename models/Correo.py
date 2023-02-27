from email.message import EmailMessage
import ssl
import smtplib

class Correos():

    @classmethod
    def NotifCitas(self, correoreceptor, userfullname, numsolic, fechacit, horacit):
        try:
            # Email empresa
            email_emisor = 'gabserra993@gmail.com'
            # Password de google
            email_password = 'jazwekwuhbhwpzbm'
            # Aqui el email receptor
            email_receptor = correoreceptor

            # Asunto
            asunto = 'Cita Agendada correctamente!'
            # Cuerpo
            cuerpo = """
            Estimado usuario {0} le escribimos del Laboratorio Chiquinquirá, nos complace anunciar que su solicitud Nro. {1} ¡Fue procesada con éxito!
            Nos complace anunciarle que su cita fue pautada para el día {2} a las {3}. Puede revisarlo ingresando en su portal en la pestaña Status.
            Gracias por confiar en nosotros, ¡Estamos para servirle!
            """.format(userfullname, numsolic, fechacit, horacit)


            em = EmailMessage()

            em['From'] = email_emisor
            em['To'] = email_receptor
            em['Subject'] = asunto
            em.set_content(cuerpo)



            contexto = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp: 
                smtp.login(email_emisor, email_password)
                smtp.sendmail(email_emisor, email_receptor, em.as_string()) 

            print("Email enviado :)")
        except Exception as ex:
            raise Exception(ex)

    
    @classmethod
    def NotifExamenes(self, correoreceptor, userfullname, numcita):
        try:
            # Email empresa
            email_emisor = 'gabserra993@gmail.com'
            # Password de google
            email_password = 'jazwekwuhbhwpzbm'
            # Aqui el email receptor
            email_receptor = correoreceptor

            # Asunto
            asunto = 'Examen agregado correctamente!'
            # Cuerpo
            cuerpo = """
            Estimado usuario {0} le notificamos del Laboratorio Chiquinquirá que su examen correspondiente a la cita {1} acaba de ser publicado.
            Puede revisar su examen ingresando en el portal. Cualquier inquietud no dude en preguntarnos. ¡Gracias por preferirnos!
            """.format(userfullname, numcita)


            em = EmailMessage()

            em['From'] = email_emisor
            em['To'] = email_receptor
            em['Subject'] = asunto
            em.set_content(cuerpo)



            contexto = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp: 
                smtp.login(email_emisor, email_password)
                smtp.sendmail(email_emisor, email_receptor, em.as_string()) 

            print("Email enviado :)")
        except Exception as ex:
            raise Exception(ex)