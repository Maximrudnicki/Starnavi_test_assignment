from sqlalchemy import func, case
from datetime import date

from repositories.comment_repository import CommentRepository
from services.comment_service import CommentService
from models.comment import Comment


"""
This code adheres to SOLID principles as follows:

1. **Single Responsibility Principle (SRP)**: 
   - `AnalyticsRepository` is solely responsible for database interactions related to comment analytics, 
   while `AnalyticsService` handles the business logic, ensuring clear separation of concerns.

2. **Open/Closed Principle (OCP)**: 
   - Both classes are open for extension (new methods can be added) but closed for modification (existing functionality remains unchanged), 
   allowing for easy enhancement without disrupting existing code.

3. **Liskov Substitution Principle (LSP)**: 
   - The `AnalyticsRepository` can be used wherever a `CommentRepository` is expected, 
   ensuring that subclasses can replace their superclasses without affecting the program's correctness.

4. **Interface Segregation Principle (ISP)**: 
   - If interfaces were used, they would be designed to contain only the methods relevant to specific implementations, 
   preventing unnecessary dependencies on unused methods.

5. **Dependency Inversion Principle (DIP)**: 
   - The `AnalyticsService` depends on the abstraction (`CommentRepository`) rather than a concrete implementation, 
   promoting flexibility and easier testing.

Overall, this structure promotes maintainability, scalability, and clarity in the codebase.
"""


class AnalyticsRepository(CommentRepository):
    def fetch_comments_analytics(self, date_from: date, date_to: date):
        with self.get_db() as db:
            return (
                db.query(
                    func.date(Comment.created_at).label("day"),
                    func.count().label("total_comments"),
                    func.sum(case((Comment.is_banned == True, 1), else_=0)).label("banned_comments"),
                )
                .filter(Comment.created_at >= date_from, Comment.created_at <= date_to)
                .group_by(func.date(Comment.created_at))
                .all()
            )


class AnalyticsService(CommentService):
    def __init__(self, comment_repository: AnalyticsRepository):
        super().__init__(comment_repository)
        self.analytics_repository = comment_repository

    def get_comments_daily_breakdown(self, date_from: date, date_to: date):
        analytics_data = self.analytics_repository.fetch_comments_analytics(date_from, date_to)
        result = []
        for record in analytics_data:
            result.append(
                {
                    "day": record.day,
                    "total_comments": record.total_comments,
                    "banned_comments": record.banned_comments,
                }
            )

        return result
