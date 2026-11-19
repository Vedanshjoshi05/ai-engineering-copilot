import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import ConnectRepository from './pages/ConnectRepository';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/connect" element={<ConnectRepository />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;