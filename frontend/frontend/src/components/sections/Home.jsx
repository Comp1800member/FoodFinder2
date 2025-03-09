import { RevealScrolling } from "../RevealScrolling"

export const Home = () => {
    return <section id="home" className="min-h-screen flex items-center justify-center relative home-b"
    >
        <RevealScrolling>
            <div className="text-center z-10 px-4">
                <h1 className="text-7xl  md:text-7xl font-Lemon font-bold mb-6 bg-green-700 bg-clip-text text-transparent leading-right">
                    Discover Food Events Near You
                </h1>
                <h1 className="bg-green-700 font-bold bg-clip-text text-transparent">
                    Find local food festivals, pop-ups, and events happening in your area
                </h1>
                <p className="text-gray-400 text-lg mb-8 max-w-lg mx-auto">
                </p>
                <div className="flex justify-center space-x-6">
                    <a href="#about" className="bg-green-700 text-white py-3 px-6 rounded font-medium transition relative overflow-hidden 
                    hover:-translate-y-0.5 hover:shadow-[0_0_15px_rgba(59, 130, 246, 0.4)]">
                        Find Events
                    </a>
                    <a href="#contact" className="border border-orange-500/50 text-yellow-500 py-3 px-6 rounded font-medium transition-all duration-200 
                    hover:-translate-y-0.5 hover:shadow-[0_0_15px_rgba(59, 130, 246, 0.2)] hover:bg-blue-500/10">
                        Ask Questions
                    </a>
                </div>
                </div>
        </RevealScrolling>
    </section>
}