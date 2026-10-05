import React, { useState, useEffect, useRef } from 'react';
import { emit_event, flush_events } from './telemetry';

export function GameShell({ gameId, title, instructions, duration, onComplete, children }) {
    const [phase, setPhase] = useState('intro'); // intro, play, end
    const timeoutRef = useRef(null);

    useEffect(() => {
        if (phase === 'play') {
            timeoutRef.current = setTimeout(() => {
                emit_event(gameId, 'timeout', 'game_timeout', { phase: 'play' }, { duration });
                handleEnd();
            }, duration * 1000);
        }
        return () => clearTimeout(timeoutRef.current);
    }, [phase, duration, gameId]);

    const handleBegin = () => {
        setPhase('play');
    };

    const handleEnd = () => {
        setPhase('end');
        flush_events();
        setTimeout(() => {
            onComplete();
        }, 2000);
    };

    if (phase === 'intro') {
        return (
            <div style={styles.container}>
                <h1>{title}</h1>
                <p>{instructions}</p>
                <button onClick={handleBegin} style={styles.button}>Begin</button>
            </div>
        );
    }

    if (phase === 'end') {
        return (
            <div style={{ ...styles.container, opacity: 0.5, transition: 'opacity 2s' }}>
                <h2>Complete</h2>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            {/* Clone children to pass handleEnd down to the game so it can finish early if appropriate (e.g. CR1 skip) */}
            {React.cloneElement(children, { onGameEnd: handleEnd, gameId })}
        </div>
    );
}

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        fontFamily: 'sans-serif'
    },
    button: {
        padding: '10px 20px',
        fontSize: '16px',
        cursor: 'pointer'
    }
};
