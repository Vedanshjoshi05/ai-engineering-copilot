import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ConnectRepository from './pages/ConnectRepository';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ConnectRepository />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;