import React from 'react';
import { Container, Typography, Box, Button, Grid, Card, CardContent } from '@mui/material';

const Main = () => {
  return (
    <Box sx={{ flexGrow: 1, py: 8 }}>
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom>
            Welcome to NotAgenticB2BSaaS
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            Your intelligent B2B SaaS solution for modern businesses
          </Typography>
          <Button variant="contained" size="large" sx={{ mt: 2 }}>
            Get Started
          </Button>
        </Box>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Feature One
                </Typography>
                <Typography color="text.secondary">
                  Powerful tools to help your business grow and scale efficiently.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Feature Two
                </Typography>
                <Typography color="text.secondary">
                  Advanced analytics and insights to make data-driven decisions.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Feature Three
                </Typography>
                <Typography color="text.secondary">
                  Seamless integration with your existing business processes.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Main;
