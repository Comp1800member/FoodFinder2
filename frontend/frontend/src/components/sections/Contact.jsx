import { RevealScrolling } from "../RevealScrolling"

export const Contact = () => {
    /*
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        message: "", 
    });

    const handleSubmit = (e) => {
        e.preventDefault()
        const SERVICE_ID = ""
        const TEMPLATE_ID = ""
        const PUBLIC_KEY = ""
        emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, e.target, PUBLIC_KEY).then((result) => {
            alert("Message sent!");
        }).catch(() => alert("Oops! Something went wrong! Please try again."));
    }
        value={formData.name}
        value={formData.email}
        value={formData.message}
    */
    return <section id="contact" className="min-h-screen flex items-center justify-center py-20">

        <RevealScrolling>
            <div className="px-4 w-150 ">
                <h2 className="text-3xl font-bold mb-8 bg-green-700 font-Lemon bg-clip-text text-transparent text-center">
                    Got Questions?
                </h2>
                <form className="space-y-6">
                    <div className="relative">
                        <input type="text" id="name" name="name" required className="w-full bg-green-50 border border-gray-100 rounded px-4 py-3 text-green-700 transition focus:outline-none focus:border-gray-400 focus:bg-gray-100"
                        placeholder="Write your name here..."
                        >

                        </input>
                    </div>
                    <div className="relative">
                        <input type="email" id="e-mail" name="e-mail" required className="w-full bg-green-50 border border-gray-100 rounded px-4 py-3 text-green-700 transition focus:outline-none focus:border-gray-400 focus:bg-gray-100"
                        placeholder="Write your e-mail here..."
                        >

                        </input>
                    </div>
                    <div className="relative">
                        <textarea id="message" name="message" required rows={5} className="w-full bg-green-50 border border-gray-100 rounded px-4 py-3 text-green-700 transition focus:outline-none focus:border-gray-400 focus:bg-gray-100"
                        placeholder="Send me a message!"
                        />
                    </div>
                    <button type="submit" className="bg-green-50 border border-gray-100 rounded px-4 py-3 text-green-700 transition focus:outline-none relative focus:border-gray-400 focus:bg-gray-100"> Send Message

                    </button>
                </form>

            </div>
        </RevealScrolling>

    </section>
}