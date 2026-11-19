
import Navbar from '../components/Navbar';
import Hero from '../sections/Hero';
import HowItWorks from '../sections/HowItWorks';

function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-gradient-to-br from-[#eef9f6] via-[#fbfcf8] to-[#fff8ee]">
      <Navbar />
      <Hero />
      <HowItWorks />
    </main>
  );
}

export default Home;
