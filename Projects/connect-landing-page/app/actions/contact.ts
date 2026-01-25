"use server"

import { Resend } from "resend"

type ContactResponse = {
  success: boolean
  message: string
}

export async function sendContactEmail(formData: FormData): Promise<ContactResponse> {
  const name = String(formData.get("name") ?? "").trim()
  const email = String(formData.get("email") ?? "").trim()
  const subject = String(formData.get("subject") ?? "").trim()
  const message = String(formData.get("message") ?? "").trim()

  if (!name || !email || !subject || !message) {
    return { success: false, message: "Please fill out all fields." }
  }

  if (!email.includes("@")) {
    return { success: false, message: "Please provide a valid email address." }
  }

  const toAddress = process.env.CONTACT_EMAIL_TO ?? "support@connect.global"
  const fromAddress = process.env.CONTACT_EMAIL_FROM ?? "Connect Contact <onboarding@resend.dev>"
  const resendKey = process.env.RESEND_API_KEY

  if (!resendKey) {
    console.log("Contact form submission", {
      name,
      email,
      subject,
      message,
      toAddress,
      fromAddress,
    })

    return { success: true, message: "Thanks! We\"ll be in touch shortly." }
  }

  try {
    const resend = new Resend(resendKey)

    await resend.emails.send({
      from: fromAddress,
      to: [toAddress],
      replyTo: email,
      subject: `Contact Form: ${subject}`,
      text: `Name: ${name}\nEmail: ${email}\nSubject: ${subject}\n\n${message}`,
    })

    return { success: true, message: "Message sent successfully. We\"ll get back to you soon." }
  } catch (error) {
    console.error("Failed to send contact email", error)
    return { success: false, message: "Something went wrong while sending your message." }
  }
}
