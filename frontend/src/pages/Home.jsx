
import Navbar from '../components/Navbar';
import Hero from '../sections/Hero';

function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-gradient-to-br from-[#eef9f6] via-[#fbfcf8] to-[#fff8ee]">
      <Navbar />
      <Hero />
    </main>
  );
}

export default Home;
