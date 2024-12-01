"use client";
import { useState, useEffect } from 'react';

type Message = {
    role: 'user' | 'assistant';
    content: string;
};

type StatsData = {
    total: number;
    high_urgency_count: number;
    top_category: string;
    top_zone: string;
    categories_distribution: { [key: string]: number };
    zones_distribution: { [key: string]: number };
    recent_issues: Array<{
        id: number;
        text: string;
        cap: string;
        category: string;
        urgency: string;
        explanation: string;
        city: string | null;
        coordinates: number[] | null;
        timestamp: string;
    }>;
};

export function ChatBot() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [statsData, setStatsData] = useState<StatsData | null>(null);

    // Carica i dati delle statistiche all'avvio
    useEffect(() => {
        fetch('http://localhost:8000/api/stats')
            .then(res => res.json())
            .then(data => setStatsData(data))
            .catch(err => console.error('Errore nel caricamento delle statistiche:', err));
    }, []);

    const sendMessage = async () => {
        if (!input.trim() || !statsData) return;

        const userMessage = input.trim();
        setInput('');
        setIsLoading(true);

        // Aggiungi il messaggio dell'utente alla chat
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        try {
            // Prepara il contesto con i dati delle statistiche
            const contextMessage = `
                Contesto attuale del sistema:
                - Totale segnalazioni: ${statsData.total}
                - Segnalazioni ad alta urgenza: ${statsData.high_urgency_count}
                - Categoria più frequente: ${statsData.top_category}
                - Zona più attiva: ${statsData.top_zone}
                
                Distribuzione categorie:
                ${Object.entries(statsData.categories_distribution)
                    .map(([cat, count]) => `- ${cat}: ${count} segnalazioni`)
                    .join('\n')}
                
                Distribuzione zone:
                ${Object.entries(statsData.zones_distribution)
                    .map(([zone, count]) => `- ${zone}: ${count} segnalazioni`)
                    .join('\n')}
                
                Ultime segnalazioni:
                ${statsData.recent_issues
                    .map(issue => `- ${issue.text} (${issue.category}, ${issue.urgency})`)
                    .join('\n')}
            `;

            // Invia la richiesta al backend
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: [
                        {
                            role: 'system',
                            content: `Sei un assistente della PA italiana che aiuta a interpretare le statistiche delle segnalazioni.
                            Puoi anche inviare email quando richiesto dall'utente.
                            
                            Contesto attuale del sistema:
                            - Totale segnalazioni: ${statsData.total}
                            - Segnalazioni ad alta urgenza: ${statsData.high_urgency_count}
                            - Categoria più frequente: ${statsData.top_category}
                            - Zona più attiva: ${statsData.top_zone}
                            
                            Distribuzione categorie:
                            ${Object.entries(statsData.categories_distribution)
                                .map(([cat, count]) => `- ${cat}: ${count} segnalazioni`)
                                .join('\n')}
                            
                            Distribuzione zone:
                            ${Object.entries(statsData.zones_distribution)
                                .map(([zone, count]) => `- ${zone}: ${count} segnalazioni`)
                                .join('\n')}
                            
                            Ultime segnalazioni:
                            ${statsData.recent_issues
                                .map(issue => `- ${issue.text} (${issue.category}, ${issue.urgency})`)
                                .join('\n')}
                            
                            Se l'utente chiede di inviare un'email, usa lo strumento email per farlo.`
                        },
                        {
                            role: 'user',
                            content: userMessage
                        }
                    ]
                }),
            });

            const data = await response.json();
            
            // Aggiungi la risposta dell'assistente alla chat
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (error) {
            console.error('Errore nell\'invio del messaggio:', error);
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: 'Mi dispiace, si è verificato un errore nella comunicazione.' 
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
            {/* Header */}
            <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Assistente PA</h2>
            </div>

            {/* Chat messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`flex ${
                            message.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg p-3 ${
                                message.role === 'user'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                            }`}
                        >
                            {message.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg p-3">
                            Sto pensando...
                        </div>
                    </div>
                )}
            </div>

            {/* Input area */}
            <div className="p-4 border-t">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Scrivi un messaggio..."
                        className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        onClick={sendMessage}
                        disabled={isLoading}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
                    >
                        Invia
                    </button>
                </div>
            </div>
        </div>
    );
}
