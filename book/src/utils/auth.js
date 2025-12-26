import { createAuthClient } from 'better-auth/client';

export const authClient = createAuthClient({
  url: "http://localhost:3000",
  secret: "3NmSGusfaN5HUGI0EhCA8pV2tyqrYeOL", // In a real app, this might be a public key or handled differently client-side
});

export const signup = async (email, password, username, skill_level) => {
  try {
    const response = await authClient.signUp.email({
      email,
      password,
      name: username,
    });
    console.log('Signup successful:', response);
    // Store custom fields in localStorage
    if (response.data?.user) {
      localStorage.setItem('user_skill_level', skill_level);
      localStorage.setItem('user_username', username);
    }
    return response.data?.user || response.user;
  } catch (error) {
    console.error('Signup failed:', error);
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const response = await authClient.signIn.email({
      email,
      password,
    });
    console.log('Login successful:', response);
    // Merge custom fields from localStorage
    const user = response.data?.user || response.user;
    if (user) {
      user.username = localStorage.getItem('user_username') || user.name || user.email;
      user.skill_level = localStorage.getItem('user_skill_level') || 'beginner';
    }
    return user;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

export const getUserProfile = async () => {
  try {
    const session = await authClient.getSession();
    if (session?.data?.user) {
      const user = session.data.user;
      // Merge custom fields from localStorage
      user.username = localStorage.getItem('user_username') || user.name || user.email;
      user.skill_level = localStorage.getItem('user_skill_level') || 'beginner';
      console.log('User profile:', user);
      return user;
    }
    return null;
  } catch (error) {
    console.error('Failed to get user profile:', error);
    return null;
  }
};

export const updateProfile = async (updates) => {
  try {
    // Update custom fields in localStorage
    if (updates.username) {
      localStorage.setItem('user_username', updates.username);
    }
    if (updates.skill_level) {
      localStorage.setItem('user_skill_level', updates.skill_level);
    }
    if (updates.preferred_language) {
      localStorage.setItem('user_preferred_language', updates.preferred_language);
    }

    // Update BetterAuth user if name is being updated
    if (updates.username) {
      try {
        await authClient.user.update({ name: updates.username });
      } catch (err) {
        console.warn('Could not update user name in BetterAuth:', err);
      }
    }

    // Get updated session
    const session = await authClient.getSession();
    const user = session?.data?.user;
    if (user) {
      user.username = localStorage.getItem('user_username') || user.name || user.email;
      user.skill_level = localStorage.getItem('user_skill_level') || 'beginner';
      user.preferred_language = localStorage.getItem('user_preferred_language') || 'en';
    }
    console.log('Profile update successful:', user);
    return user;
  } catch (error) {
    console.error('Profile update failed:', error);
    throw error;
  }
};

export const logout = async () => {
  try {
    await authClient.signOut();
    // Clear custom fields from localStorage
    localStorage.removeItem('user_username');
    localStorage.removeItem('user_skill_level');
    localStorage.removeItem('user_preferred_language');
    console.log('Logout successful');
  } catch (error) {
    console.error('Logout failed:', error);
    throw error;
  }
};

// Placeholder for database interaction for custom profile fields beyond BetterAuth's user_metadata
// This would typically be a serverless function interacting directly with Neon Postgres
export const updateCustomUserProfile = async (userId, updates) => {
  console.warn('Custom user profile updates require a server-side component (e.g., serverless function) to interact with Neon Postgres directly.');
  // Example: fetch('/api/updateUserProfile', { method: 'POST', body: JSON.stringify({ userId, updates }) });
  return Promise.resolve(null);
};