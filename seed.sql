INSERT INTO public.users (username, email, password, is_banned, auto_reply_enabled, auto_reply_delay)
VALUES 
    ('user1', 'user1@example.com', 'password1', FALSE, TRUE, 60),
    ('user2', 'user2@example.com', 'password2', FALSE, TRUE, 60),
    ('user3', 'user3@example.com', 'password3', FALSE, TRUE, 60);
	
	   
INSERT INTO public.posts (title, text, created_at, updated_at, author_id)
VALUES 
    ('First Post', 'This is the first post.', NOW(), NOW(), (SELECT id FROM public.users WHERE username = 'user1')),
    ('Second Post', 'This is the second post.', NOW(), NOW(), (SELECT id FROM public.users WHERE username = 'user1')),
    ('Third Post', 'This is the third post.', NOW(), NOW(), (SELECT id FROM public.users WHERE username = 'user3'));
	   
	   
INSERT INTO public.comments (post_id, user_id, text, created_at, is_banned, banned_at)
VALUES 
  ((SELECT id FROM public.posts WHERE title = 'First Post'),
   (SELECT id FROM public.users WHERE username = 'user1'),
   'First comment on first post', '2024-09-17', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'First Post'),
   (SELECT id FROM public.users WHERE username = 'user2'),
   'Second comment on first post', '2024-09-17', TRUE, '2024-09-17'),
  ((SELECT id FROM public.posts WHERE title = 'First Post'),
   (SELECT id FROM public.users WHERE username = 'user1'),
   'Third comment on first post', '2024-09-18', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Second Post'),
   (SELECT id FROM public.users WHERE username = 'user3'),
   'First comment on second post', '2024-09-19', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Second Post'),
   (SELECT id FROM public.users WHERE username = 'user2'),
   'Second comment on second post', '2024-09-19', TRUE, '2024-09-19'),
  ((SELECT id FROM public.posts WHERE title = 'Third Post'),
   (SELECT id FROM public.users WHERE username = 'user1'),
   'First comment on third post', '2024-09-20', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Third Post'),
   (SELECT id FROM public.users WHERE username = 'user3'),
   'Second comment on third post', '2024-09-20', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'First Post'),
   (SELECT id FROM public.users WHERE username = 'user1'),
   'Another comment on first post', '2024-09-21', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Second Post'),
   (SELECT id FROM public.users WHERE username = 'user2'),
   'Another comment on second post', '2024-09-21', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Third Post'),
   (SELECT id FROM public.users WHERE username = 'user3'),
   'Another comment on third post', '2024-09-22', TRUE, '2024-09-22'),
  ((SELECT id FROM public.posts WHERE title = 'First Post'),
   (SELECT id FROM public.users WHERE username = 'user2'),
   'Yet another comment on first post', '2024-09-22', FALSE, NULL),
  ((SELECT id FROM public.posts WHERE title = 'Second Post'),
   (SELECT id FROM public.users WHERE username = 'user1'),
   'Yet another comment on second post', '2024-09-23', TRUE, '2024-09-23'),
  ((SELECT id FROM public.posts WHERE title = 'Third Post'), 
   (SELECT id FROM public.users WHERE username = 'user2'),
   'Yet another comment on third post', '2024-09-24', FALSE, NULL);