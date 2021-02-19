import Link from 'next/link'
import styles from './Footer.module.css'

export default function Footer() {
    return <footer className={styles.footer}>
        <Link href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app">
            <a target="_blank" rel="noopener noreferrer" >
                Created by&nbsp;{" "}
                <Link href="https://github.com/skend">
                    <a className={styles.github}>skend</a>
                </Link>
            </a>
        </Link>
    </footer>
}