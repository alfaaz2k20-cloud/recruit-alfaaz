import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function CR3_BrokenToolExperiment({ onGameEnd, gameId }) {
    const [puzzle, setPuzzle] = useState(1);
    const [tools, setTools] = useState({ trapBlock: {x: 0, y: 0}, block2: {x: 10, y: 0} });
    const hasFailedRef = useRef(false);
    
    useEffect(() => {
        if (puzzle > 2) {
            onGameEnd();
        }
    }, [puzzle]);

    const handleRelease = () => {
        const distance = Math.random(); // Simulate configuration distance
        emit_event(gameId, puzzle.toString(), 'attempt_config', {}, { positions: tools });
        emit_event(gameId, puzzle.toString(), 'release', {}, { is_post_fail: hasFailedRef.current, config_distance: distance });
        
        const isSuccess = Math.random() > 0.7; // Harder
        emit_event(gameId, puzzle.toString(), 'sim_outcome', {}, { reason: isSuccess ? 'success' : 'fall', progress: 0.5 });
        
        if (isSuccess) {
            hasFailedRef.current = false;
            setTimeout(() => setPuzzle(p => p + 1), 1000);
        } else {
            hasFailedRef.current = true;
        }
    };

    const handleSkip = () => {
        emit_event(gameId, puzzle.toString(), 'skip', {}, {});
        hasFailedRef.current = false;
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
            <p>Get the orb to the pad. Watch out for traps.</p>
            <div style={{ height: '150px', border: '1px dashed black', position: 'relative', margin: '20px 0' }}>
                <div style={{ position: 'absolute', top: 10, left: 10 }}>🔮</div>
                <div style={{ position: 'absolute', bottom: 10, right: 10 }}>⬛</div>
                {Object.entries(tools).map(([tool, pos]) => (
                    <div 
                        key={tool} 
                        style={{ position: 'absolute', top: 50 + pos.y, left: 50 + pos.x, cursor: 'pointer', background: tool === 'trapBlock' ? '#fcc' : '#ccc', padding: '5px' }}
                        onClick={() => handleMove(tool, 15, 5)}
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
