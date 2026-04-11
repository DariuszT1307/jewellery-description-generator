import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

/**
 * Renderuje tekst z prostym formatowaniem markdown:
 * - **tekst** → <strong>tekst</strong>
 * - podwójny enter → nowy akapit
 * - pojedynczy enter → <br />
 * - linia zaczynająca się od "- " → element listy
 */
function renderDescription(text) {
  if (!text) return null

  const paragraphs = text.split('\n\n')

  return paragraphs.map((para, pIdx) => {
    const lines = para.split('\n')

    // Sprawdź czy akapit to lista punktorów
    const isList = lines.every(l => l.trim() === '' || l.trim().startsWith('- '))
    if (isList && lines.some(l => l.trim().startsWith('- '))) {
      return (
        <ul key={pIdx} style={{ margin: '0.4rem 0 0.4rem 1.2rem', padding: 0 }}>
          {lines
            .filter(l => l.trim().startsWith('- '))
            .map((l, lIdx) => (
              <li key={lIdx}>{applyInline(l.trim().slice(2))}</li>
            ))}
        </ul>
      )
    }

    // Zwykły akapit z ewentualnymi <br /> między liniami
    const content = lines.map((line, lIdx) => (
      <span key={lIdx}>
        {applyInline(line)}
        {lIdx < lines.length - 1 && <br />}
      </span>
    ))

    return <p key={pIdx} style={{ margin: '0.5rem 0' }}>{content}</p>
  })
}

/** Zamienia **tekst** na <strong>tekst</strong> w obrębie jednej linii */
function applyInline(text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    return part
  })
}

function App() {
  const [formData, setFormData] = useState({
    productType: 'bracelet',
    stone: '',
    stone2: '',
    productName: '',
    keywords: '',
    notes: '',
    images: []
  })

  const [twoStones, setTwoStones] = useState(false)

  const [stones, setStones] = useState([])
  const [stonesLoading, setStonesLoading] = useState(true)
  const [stonesError, setStonesError] = useState(null)

  const [payload, setPayload] = useState(null)
  const [generatedResult, setGeneratedResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/stones`)
      .then(res => {
        if (!res.ok) throw new Error(`Błąd serwera: ${res.status}`)
        return res.json()
      })
      .then(data => {
        setStones(data.stones)
        if (data.stones.length > 0) {
          setFormData(prev => ({ ...prev, stone: data.stones[0].value }))
        }
      })
      .catch(err => {
        setStonesError(err.message || 'Nie udało się pobrać listy kamieni')
      })
      .finally(() => setStonesLoading(false))
  }, [])

  const productTypes = [
    { value: 'necklace', label: 'Naszyjnik' },
    { value: 'ring', label: 'Pierścionek' },
    { value: 'bracelet', label: 'Bransoletka' },
    { value: 'earrings', label: 'Kolczyki' }
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

    if (twoStones && !formData.stone2) {
      alert('Wybierz drugi kamień lub odznacz opcję "Użyj dwóch kamieni"')
      return
    }

    if (twoStones && formData.stone2 === formData.stone) {
      alert('Drugi kamień musi być inny niż pierwszy')
      return
    }

    const requestBody = {
      productType: formData.productType,
      stone: formData.stone,
      ...(twoStones && formData.stone2 ? { stone2: formData.stone2 } : {}),
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
      const response = await fetch(`${API_BASE}/generate`, {
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
            {stonesLoading ? (
              <select disabled><option>Ładowanie kamieni...</option></select>
            ) : stonesError ? (
              <div>
                <select disabled><option>Błąd ładowania</option></select>
                <span style={{ color: '#ff6b6b', fontSize: '0.85rem' }}>
                  {stonesError} —{' '}
                  <button
                    type="button"
                    onClick={() => window.location.reload()}
                    style={{ background: 'none', border: 'none', color: '#ff6b6b', cursor: 'pointer', textDecoration: 'underline', padding: 0 }}
                  >
                    odśwież
                  </button>
                </span>
              </div>
            ) : (
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
            )}
          </div>

          <div className="form-group" style={{ flexDirection: 'row', alignItems: 'center', gap: '0.6rem' }}>
            <input
              id="twoStones"
              type="checkbox"
              checked={twoStones}
              onChange={e => {
                setTwoStones(e.target.checked)
                if (!e.target.checked) setFormData(prev => ({ ...prev, stone2: '' }))
              }}
              style={{ width: 'auto', cursor: 'pointer' }}
            />
            <label htmlFor="twoStones" style={{ marginBottom: 0, cursor: 'pointer' }}>
              Użyj dwóch kamieni
            </label>
          </div>

          {twoStones && (
            <div className="form-group">
              <label htmlFor="stone2">Drugi kamień *</label>
              {stonesLoading ? (
                <select disabled><option>Ładowanie kamieni...</option></select>
              ) : stonesError ? (
                <select disabled><option>Błąd ładowania</option></select>
              ) : (
                <select
                  id="stone2"
                  name="stone2"
                  value={formData.stone2}
                  onChange={handleInputChange}
                  required={twoStones}
                >
                  <option value="">— wybierz drugi kamień —</option>
                  {stones
                    .filter(s => s.value !== formData.stone)
                    .map(stone => (
                      <option key={stone.value} value={stone.value}>
                        {stone.label}
                      </option>
                    ))}
                </select>
              )}
            </div>
          )}

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

            <h4 style={{ marginTop: '1.2rem', marginBottom: '0.4rem' }}>Krótki opis</h4>
            <div>{renderDescription(generatedResult.shortDescription)}</div>

            <h4 style={{ marginTop: '1.2rem', marginBottom: '0.4rem' }}>Pełny opis</h4>
            <div>{renderDescription(generatedResult.longDescription)}</div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
