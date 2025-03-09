import { useEffect } from "react"
import logo from "../assets/images/6.jpg"

export const Navbar = ({menuOpen, setMenuOpen}) => {

    useEffect(() => {
        document.body.style.overflow = menuOpen ? "hidden" : ""
    }, [menuOpen]);

    return <nav className="fixed top-0 w-full z-40 bg-white backdrop-blur-lg border-b border-white/10 shadow-lg">
        <div className="max-w-5xcl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
                <a href="#home" className="font-mono flex text-xl  font-bold text-white">
                    {" "}
                    <img id="raccoon"src={logo} alt="racoon" className="h-16 "/>
                    <span className="text-green-600 py-5">FoodEvents</span>{" "}
                    </a>
                <div className="w-7 h-5 relative cursor-pointer z-40 md:hidden" onClick={() => setMenuOpen((prev) => !prev)}>
                    &#9776;
                </div>
                <div className="hidden md:flex items-center space-x-8">
                    <a 
                        href="#home" 
                        className="text-black hover-text-white transition-colors"
                    > 
                        {" "}
                        Home{" "} 
                    </a>
                    <a 
                        href="#about" 
                        className="text-black hover-text-white transition-colors"
                    > 
                        {" "}
                        Find Events{" "} 
                    </a>
                    <a 
                        href="#contact" 
                        className="text-black hover-text-white transition-colors"
                    > 
                        {" "}
                        Contact Us{" "} 
                    </a>
                    {/*
                    <a 
                        href="#contact" 
                        className="text-black hover-text-white transition-colors"
                    > 
                        {" "}
                        Donate{" "} 
                    </a>
                    */}
                </div>
            </div>
        </div>
        {" "}
    </nav>
}