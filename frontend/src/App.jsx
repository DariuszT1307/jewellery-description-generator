import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    productType: 'necklace',
    stone: 'amethyst',
    productName: '',
    keywords: '',
    notes: '',
    images: []
  })
  
  const [payload, setPayload] = useState(null)
  const [generatedResult, setGeneratedResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const productTypes = [
    { value: 'necklace', label: 'Naszyjnik' },
    { value: 'ring', label: 'Pierścionek' },
    { value: 'bracelet', label: 'Bransoletka' },
    { value: 'earrings', label: 'Kolczyki' }
  ]

  const stones = [
    { value: 'amethyst', label: 'Ametyst' },
    { value: 'rose_quartz', label: 'Kwarc różowy' },
    { value: 'citrine', label: 'Cytryn' },
    { value: 'clear_quartz', label: 'Kwarc przejrzysty' },
    { value: 'obsidian', label: 'Obsydian' },
    { value: 'lapis_lazuli', label: 'Lazuryt' },
    { value: 'malachite', label: 'Malachit' },
    { value: 'tourmaline', label: 'Turmalin' }
  ]

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files)
    setFormData(prev => ({
      ...prev,
      images: files
    }))
  }

  const handleGeneratePayload = async (e) => {
    e.preventDefault()
    
    if (!formData.productName.trim()) {
      alert('Nazwa produktu jest wymagana')
      return
    }

    const requestBody = {
      productType: formData.productType,
      stone: formData.stone,
      productName: formData.productName,
      keywords: formData.keywords || null,
      notes: formData.notes || null,
      images: formData.images.map(img => ({
        name: img.name,
        size: img.size,
        type: img.type
      }))
    }

    setPayload(requestBody)
    setError(null)
    setGeneratedResult(null)
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        throw new Error('Błąd serwera: ' + response.status)
      }

      const data = await response.json()
      setGeneratedResult(data)
    } catch (err) {
      setError(err.message || 'Nie udało się wygenerować opisu')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <main className="app-main">
        <form onSubmit={handleGeneratePayload} className="form-container dark-form">
          <div className="form-group">
            <label htmlFor="productType">Typ produktu *</label>
            <select
              id="productType"
              name="productType"
              value={formData.productType}
              onChange={handleInputChange}
              required
            >
              {productTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="stone">Kamień *</label>
            <select
              id="stone"
              name="stone"
              value={formData.stone}
              onChange={handleInputChange}
              required
            >
              {stones.map(stone => (
                <option key={stone.value} value={stone.value}>
                  {stone.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="productName">Nazwa robocza *</label>
            <input
              id="productName"
              type="text"
              name="productName"
              value={formData.productName}
              onChange={handleInputChange}
              placeholder="np. Naszyjnik z ametystu na srebrnym drucie"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="keywords">Słowa kluczowe / motywy</label>
            <textarea
              id="keywords"
              name="keywords"
              value={formData.keywords}
              onChange={handleInputChange}
              placeholder="np. naturalne, energetyczne, minimalistyczne"
              rows="3"
            />
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notatki dodatkowe</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              placeholder="np. specjalne cechy produktu, inspiracje"
              rows="3"
            />
          </div>

          <div className="form-group">
            <label htmlFor="images">Zdjęcia referencyjne</label>
            <input
              id="images"
              type="file"
              name="images"
              multiple
              accept="image/*"
              onChange={handleImageUpload}
            />
            {formData.images.length > 0 && (
              <div className="images-preview">
                <p>Wybrane pliki ({formData.images.length}):</p>
                <ul>
                  {formData.images.map((img, idx) => (
                    <li key={idx}>{img.name}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <button type="submit" className="submit-button">
            Generuj opis
          </button>
        </form>

        {payload && (
          <div className="payload-preview">
            <h2>Podgląd payloadu</h2>
            <pre>{JSON.stringify(payload, null, 2)}</pre>
          </div>
        )}

        {loading && <p>Trwa generowanie opisu...</p>}
        {error && <p style={{ color: '#ff6b6b' }}>Błąd: {error}</p>}

        {generatedResult && (
          <div className="payload-preview">
            <h2>Wynik wygenerowanego opisu</h2>
            <h3>{generatedResult.title}</h3>
            <p>{generatedResult.shortDescription}</p>
            <ul>
              {generatedResult.bullets.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
            <p>{generatedResult.longDescription}</p>
            <h4>Specyfikacja</h4>
            <pre>{JSON.stringify(generatedResult.specs, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
