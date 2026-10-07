from features.tracker.model import StressRecord

class StressRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, record: StressRecord):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stress_logs (user_id, timestamp, 
            level_code, task, note)
            VALUES (?, ?, ?, ?, ?)
        """, (record.user_id, record.timestamp, record.level_code, record.task, record.note))
        conn.commit()
        record.id = cursor.lastrowid
        conn.close()
        return record

    def get_all_by_user(self, user_id: int):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, timestamp, level_code, task, note
            FROM stress_logs
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            StressRecord(
                id=r["id"], user_id=r["user_id"], timestamp=r["timestamp"],
                level_code=r["level_code"], task=r["task"], note=r["note"]
            )
            for r in rows
        ]

    def update(self, record_id: int, user_id: int, new_level: str, new_task: str, new_note: str):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stress_logs
            SET level_code = ?, task = ?, note = ?
            WHERE id = ? AND user_id = ?
        """, (new_level, new_task, new_note, record_id, user_id))
        conn.commit()
        conn.close()

    def delete(self, record_id: int, user_id: int):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stress_logs WHERE id = ? AND user_id = ?", (record_id, user_id))
        conn.commit()
        conn.close()