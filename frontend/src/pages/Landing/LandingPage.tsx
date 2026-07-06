
import { Footer } from "../../components/common/Footer";
import Navbar from "../../components/common/Navbar";

import { CTA } from "./sections/CTA";
import  Features  from "./sections/Features";
import  Hero from "./sections/Hero";
import  HowItWorks  from "./sections/HowItWorks";


function LandingPage() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <CTA />
      <Footer />
    </>
  );
}

export default LandingPage;