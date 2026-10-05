import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function CR1_BrokenToolBuild({ onGameEnd, gameId }) {
    const [puzzle, setPuzzle] = useState(1);
    const [tools, setTools] = useState({ block1: {x: 0, y: 0}, block2: {x: 10, y: 0} });
    
    useEffect(() => {
        if (puzzle > 2) {
            onGameEnd();
        }
    }, [puzzle]);

    const handleRelease = () => {
        // simulate physics outcome
        const isSuccess = Math.random() > 0.5;
        const family = Math.random() > 0.5 ? 'bridge' : 'ramp'; // simplistic heuristic for distinct families
        emit_event(gameId, puzzle.toString(), 'release', {}, { strategy_family: family });
        emit_event(gameId, puzzle.toString(), 'sim_outcome', {}, { reason: isSuccess ? 'success' : 'fall', progress: 0.8 });
        
        if (isSuccess || Math.random() > 0.8) {
            // move to next puzzle
            setTimeout(() => setPuzzle(p => p + 1), 1000);
        }
    };

    const handleSkip = () => {
        emit_event(gameId, puzzle.toString(), 'skip', {}, {});
        setPuzzle(p => p + 1);
    };

    const handleMove = (tool, dx, dy) => {
        setTools(prev => ({
            ...prev,
            [tool]: { x: prev[tool].x + dx, y: prev[tool].y + dy }
        }));
        emit_event(gameId, puzzle.toString(), 'tool_move', {}, { tool });
    };

    if (puzzle > 2) return null;

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Get the orb to the pad. Use what you have.</p>
            <div style={{ height: '150px', border: '1px dashed black', position: 'relative', margin: '20px 0' }}>
                <div style={{ position: 'absolute', top: 10, left: 10 }}>🔮</div>
                <div style={{ position: 'absolute', bottom: 10, right: 10 }}>⬛</div>
                {Object.entries(tools).map(([tool, pos]) => (
                    <div 
                        key={tool} 
                        style={{ position: 'absolute', top: 50 + pos.y, left: 50 + pos.x, cursor: 'pointer', background: '#ccc', padding: '5px' }}
                        onClick={() => handleMove(tool, 10, 10)}
                    >
                        {tool}
                    </div>
                ))}
            </div>
            <button onClick={handleRelease} style={{ marginRight: '10px' }}>Release</button>
            <button onClick={handleSkip}>Skip</button>
        </div>
    );
}
